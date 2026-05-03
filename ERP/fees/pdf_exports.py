import io
import os
import base64
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from xhtml2pdf import pisa

from accounts.decorators import role_required
from core.models import AcademicYear, Division
from .models import FeeStructure, FeeType

_STAFF_VIEW = ('SUPER_ADMIN', 'ADMIN', 'ACCOUNTANT', 'STAFF')

# Fee type category constants we want to map to specific columns
_CAT_ENTRANCE    = FeeType.ENTRANCE_EXAM
_CAT_REGISTRATION = FeeType.REGISTRATION
_CAT_RESERVATION  = FeeType.RESERVATION
_CAT_TUITION      = FeeType.TUITION

# Installment categories — shown as separate columns
_INSTALLMENT_CATS = {
    'FIRST':  None,   # will be matched dynamically
    'SECOND': None,
    'THIRD':  None,
}

VAT_RATE = Decimal('0.15')


def _logo_base64():
    """Return a base64 data URI for the school logo — works reliably in xhtml2pdf."""
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logo_path = os.path.normpath(os.path.join(base, '..', 'logo', 'image.png'))
    try:
        with open(logo_path, 'rb') as f:
            encoded = base64.b64encode(f.read()).decode('utf-8')
        return f'data:image/png;base64,{encoded}'
    except Exception:
        return None


def _build_row(structure, fee_types_map):
    """
    Given a FeeStructure and a {category: FeeType} map,
    build a dict with computed amounts for each column.
    """
    items = {item.fee_type.category: item.amount
             for item in structure.items.select_related('fee_type').all()}

    entrance    = items.get(_CAT_ENTRANCE,    Decimal('0.00'))
    registration = items.get(_CAT_REGISTRATION, Decimal('0.00'))
    reservation  = items.get(_CAT_RESERVATION,  Decimal('0.00'))
    gross_tuition = items.get(_CAT_TUITION,     Decimal('0.00'))

    # Detect installment amounts — any fee type whose name contains keywords
    # Alternatively, look for fee types named like "1st Installment" etc.
    # We'll grab them by order from remaining amounts
    other_items = [
        (ft_cat, amt) for ft_cat, amt in items.items()
        if ft_cat not in (_CAT_ENTRANCE, _CAT_REGISTRATION, _CAT_RESERVATION, _CAT_TUITION)
    ]

    # Sort by fee type name to get consistent order
    installments = sorted(other_items, key=lambda x: str(x[0]))

    first_inst  = installments[0][1] if len(installments) > 0 else Decimal('0.00')
    second_inst = installments[1][1] if len(installments) > 1 else Decimal('0.00')
    third_inst  = installments[2][1] if len(installments) > 2 else Decimal('0.00')

    # For gross: if no separate gross tuition, use all non-entrance/registration amounts combined
    if gross_tuition == Decimal('0.00'):
        gross_tuition = sum(
            amt for cat, amt in items.items()
            if cat not in (_CAT_ENTRANCE, _CAT_REGISTRATION, _CAT_RESERVATION)
        )

    # Net tuition = gross (no group discount tracked in FeeStructure)
    net_tuition = gross_tuition

    # Non-Saudi = net + 15% VAT on tuition
    vat_amount    = (net_tuition * VAT_RATE).quantize(Decimal('0.01'))
    non_saudi_net = (net_tuition + vat_amount).quantize(Decimal('0.01'))

    return {
        'grade':          structure.grade.name,
        'entrance_exam':  entrance,
        'registration':   registration,
        'gross_tuition':  gross_tuition,
        'group_disc_amt': Decimal('0.00'),   # group discount not stored in FeeStructure
        'tuition_net':    net_tuition,        # ← matches template's r.tuition_net
        'reservation':    reservation,
        'first_inst':     first_inst,
        'second_inst':    second_inst,
        'third_inst':     third_inst,
        # Saudi = net tuition (VAT zero-rated)
        'saudi_net':      net_tuition,
        # Non-Saudi = net tuition + VAT
        'vat_amount':     vat_amount,
        'non_saudi_net':  non_saudi_net,
    }


@login_required
@role_required(*_STAFF_VIEW)
def fee_structure_export_group_pdf(request):
    division_id    = request.GET.get('division', '').strip()
    year_id        = request.GET.get('year', '').strip()
    structure_type = request.GET.get('type', 'regular').strip().lower()

    if not division_id:
        return HttpResponse('Missing required parameter: division', status=400)

    try:
        division = Division.objects.get(pk=division_id)
    except Division.DoesNotExist:
        return HttpResponse('Division not found', status=404)

    year = None
    if year_id:
        try:
            year = AcademicYear.objects.get(pk=year_id)
        except AcademicYear.DoesNotExist:
            return HttpResponse('Academic Year not found', status=404)

    # Fetch structures
    qs_filter = dict(grade__division=division, structure_type=structure_type)
    if year:
        qs_filter['academic_year'] = year

    structures = (
        FeeStructure.objects
        .filter(**qs_filter)
        .select_related('grade', 'academic_year', 'grade__division')
        .prefetch_related('items__fee_type')
        .order_by('grade__order', 'grade__name')
    )

    if not structures.exists():
        return HttpResponse(
            f'No fee structures found for {division.name} / {structure_type}.',
            status=404
        )

    # Collect all fee type categories used across all structures
    all_fee_types = {}
    for s in structures:
        for item in s.items.all():
            all_fee_types[item.fee_type.category] = item.fee_type

    # Build per-grade rows
    rows = []
    has_third = False
    for s in structures:
        row = _build_row(s, all_fee_types)
        if row['third_inst'] > Decimal('0.00'):
            has_third = True
        rows.append(row)

    # Determine description from structure name or auto-generate
    type_label = {
        'regular': 'REGULAR',
        'new':     'NEW STUDENT',
        'other':   'OTHER',
    }.get(structure_type, structure_type.upper())

    year_label = str(year) if year else 'All Years'
    description = f"{type_label} PRICE STRUCTURE FOR {year_label} - {division.name.upper()}"

    # Determine num_payments from actual data
    num_payments = 2
    if has_third:
        num_payments = 3

    # Compute header-level registration/entrance/reservation from first row
    first_row = rows[0] if rows else {}

    context = {
        'division':        division,
        'year':            year_label,
        'structure_type':  type_label,
        'description':     description,
        'group_discount':  'NO',
        'group_disc_pct':  Decimal('0.00'),
        'num_payments':    num_payments,
        'registration_fee': first_row.get('registration', Decimal('0.00')),
        'reservation_fee':  first_row.get('reservation', Decimal('0.00')),
        'entrance_exam':    first_row.get('entrance_exam', Decimal('0.00')),
        'includes_books':  'NO',
        'from_year':       year_label,
        'to_year':         None,
        'vat_pct':         Decimal('15.00'),
        'rows':            rows,
        'has_third':       has_third,
        'now':             timezone.now().strftime('%d-%b-%Y %I:%M %p'),
        'logo_src':        _logo_base64(),
    }

    html = render_to_string('fees/fee_structure_group_pdf.html', context)
    buf = io.BytesIO()
    pisa.pisaDocument(io.BytesIO(html.encode('UTF-8')), buf)

    div_name = division.name.replace(' ', '_')
    filename = f"tuition_fee_{div_name}_{year_label}_{structure_type}.pdf"
    response = HttpResponse(buf.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
