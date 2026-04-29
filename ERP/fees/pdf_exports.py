from django.utils import timezone
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.http import HttpResponse
from decimal import Decimal
import io
from .models import FeeStructure, FeeType, AcademicYear, Division

from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required

# Define _STAFF_VIEW here to fix NameError (keep in sync with views.py)
_STAFF_VIEW = ('SUPER_ADMIN', 'ADMIN', 'ACCOUNTANT', 'STAFF')

@login_required
@role_required(*_STAFF_VIEW)
def fee_structure_export_group_pdf(request):
    division_id    = request.GET.get('division', '').strip()
    year_id        = request.GET.get('year', '').strip()
    structure_type = request.GET.get('type', '').strip().lower()

    if not (division_id and structure_type):
        return HttpResponse('Missing required parameters: division, type', status=400)

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

    structure_filter = dict(
        grade__division=division,
        structure_type=structure_type,
    )
    if year:
        structure_filter['academic_year'] = year

    structures = (
        FeeStructure.objects
        .filter(**structure_filter)
        .select_related('grade', 'academic_year', 'grade__division')
        .prefetch_related('items__fee_type')
        .order_by('grade__order', 'grade__name')
    )
    if not structures.exists():
        return HttpResponse('No fee structures found for the given parameters.', status=404)

    # Collect all distinct fee types present across these structures (ordered)
    fee_types_map = {}
    for s in structures:
        for item in s.items.all():
            fee_types_map[item.fee_type_id] = item.fee_type
    ordered_fee_types = sorted(fee_types_map.values(), key=lambda ft: (ft.category, ft.name))

    # Prepare per-structure details for template
    structure_rows = []
    for s in structures:
        items_by_type = {item.fee_type_id: item.amount for item in s.items.all()}
        # Try to get extra fields if present
        row = {
            'grade': s.grade,
            'name': s.name or '',
            'get_frequency_display': s.get_frequency_display(),
            'group_discount': getattr(s, 'group_discount', ''),
            'vat_pct': getattr(s, 'vat_pct', '15'),
            'due_date': getattr(s, 'due_date', ''),
            'structure_code': getattr(s, 'structure_code', ''),
            'description': getattr(s, 'description', ''),
            'items_by_type': items_by_type,
        }
        # Totals
        total_before_vat = Decimal('0.00')
        total_with_vat   = Decimal('0.00')
        for ft in ordered_fee_types:
            amt = items_by_type.get(ft.pk, Decimal('0.00'))
            total_before_vat += amt
            if getattr(ft, 'is_taxable', False):
                try:
                    vat = Decimal(row['vat_pct'] or '15')
                except Exception:
                    vat = Decimal('15')
                total_with_vat += (amt * (1 + vat/100)).quantize(Decimal('0.01'))
            else:
                total_with_vat += amt
        row['total_before_vat'] = str(total_before_vat.quantize(Decimal('0.01')))
        row['total_with_vat'] = str(total_with_vat.quantize(Decimal('0.01')))
        structure_rows.append(row)

    html = render_to_string('fees/fee_structure_group_pdf.html', {
        'division': division,
        'year': year or 'All Years',
        'structure_type': structure_type,
        'fee_types': ordered_fee_types,
        'structures': structure_rows,
        'now': timezone.now().strftime('%Y-%m-%d %H:%M'),
    })
    result = io.BytesIO()
    pisa_status = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
    filename = f"fee_structure_{division.name.replace(' ','_')}_{year or 'all_years'}_{structure_type}.pdf"
    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
