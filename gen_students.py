"""One-shot script: generate 1000 student records per division as a CSV.
Run with:  python manage.py shell < ..\gen_students.py
"""
import csv, random, re
from datetime import date
from core.models import Division, Grade, Section, AcademicYear, StudyMode

random.seed(20260518)

OUT = r"e:\ERP_SYSTEM\students_import_3000.csv"

# ── Name pools ────────────────────────────────────────────────
SAUDI_M = ['Mohammed','Abdullah','Omar','Faisal','Khalid','Salman','Turki','Yazeed','Sultan','Bandar',
           'Nawaf','Saud','Majed','Fahad','Naif','Bader','Hatim','Hassan','Ibrahim','Yousef',
           'Saif','Talal','Waleed','Ziyad','Anas','Adel','Ali','Hamad','Ammar','Raed']
SAUDI_F = ['Noura','Reema','Sara','Dalal','Hessa','Lujain','Dana','Raghad','Lama','Maha',
           'Aljawhara','Latifa','Aisha','Mariam','Fatima','Layla','Hanan','Norah','Wafa','Salma',
           'Manal','Asma','Ghada','Amal','Reem','Shaden','Joud','Renad','Tala','Jana']
LASTNAMES = ['Al-Zahrani','Al-Qahtani','Al-Shehri','Al-Ghamdi','Al-Maliki','Al-Dosari','Al-Harbi',
             'Al-Otaibi','Al-Sulami','Al-Rashid','Al-Anazi','Al-Mutairi','Al-Fayez','Al-Sudais',
             'Al-Saud','Al-Hashemi','Al-Tamimi','Al-Hussein','Al-Yamani','Al-Sabah']
EXPAT_M = ['Yusuf','Imran','Hamza','Talha','Bilal','Hassan','Ahmed','Ismail','Zain','Adam',
           'Daniel','Michael','David','James','John','Tariq','Junaid','Ayaan','Aryan','Rohan',
           'Vihaan','Kabir','Zayn','Mustafa','Faris']
EXPAT_F = ['Aisha','Fatima','Zainab','Khadija','Mariam','Nayla','Hira','Sana','Sadia','Mehek',
           'Anaya','Aliya','Priya','Anika','Diya','Riya','Saanvi','Anvi','Sofia','Maya',
           'Layla','Nour','Zoe','Sophia','Olivia','Emma']
EXPAT_LAST = ['Khan','Ahmed','Ali','Hassan','Hussain','Malik','Sheikh','Siddiqui','Shaikh',
              'Rahman','Mahmood','Sharma','Patel','Gupta','Singh','Kumar','Reddy','Ibrahim',
              'Mansoor','Saleh','Habib','Chen','Wang','Garcia','Kim','Smith','Brown']

AR_FIRST = {
    'Mohammed':'محمد','Abdullah':'عبدالله','Omar':'عمر','Faisal':'فيصل','Khalid':'خالد',
    'Salman':'سلمان','Turki':'تركي','Yazeed':'يزيد','Sultan':'سلطان','Bandar':'بندر',
    'Nawaf':'نواف','Saud':'سعود','Majed':'ماجد','Fahad':'فهد','Naif':'نايف','Bader':'بدر',
    'Hatim':'حاتم','Hassan':'حسن','Ibrahim':'إبراهيم','Yousef':'يوسف','Saif':'سيف','Talal':'طلال',
    'Waleed':'وليد','Ziyad':'زياد','Anas':'أنس','Adel':'عادل','Ali':'علي','Hamad':'حمد',
    'Ammar':'عمار','Raed':'رائد',
    'Noura':'نورة','Reema':'ريما','Sara':'سارة','Dalal':'دلال','Hessa':'حصة','Lujain':'لجين',
    'Dana':'دانا','Raghad':'رغد','Lama':'لمى','Maha':'مها','Aljawhara':'الجوهرة','Latifa':'لطيفة',
    'Aisha':'عائشة','Mariam':'مريم','Fatima':'فاطمة','Layla':'ليلى','Hanan':'حنان','Norah':'نورة',
    'Wafa':'وفاء','Salma':'سلمى','Manal':'منال','Asma':'أسماء','Ghada':'غادة','Amal':'أمل',
    'Reem':'ريم','Shaden':'شادن','Joud':'جود','Renad':'رناد','Tala':'تالا','Jana':'جنى',
    'Yusuf':'يوسف','Imran':'عمران','Hamza':'حمزة','Talha':'طلحة','Bilal':'بلال','Ahmed':'أحمد',
    'Ismail':'إسماعيل','Zain':'زين','Adam':'آدم','Daniel':'دانيال','Michael':'مايكل','David':'ديفيد',
    'James':'جيمس','John':'جون','Tariq':'طارق','Junaid':'جنيد','Ayaan':'أيان','Aryan':'آريان',
    'Rohan':'روهان','Vihaan':'فيهان','Kabir':'كبير','Zayn':'زين','Mustafa':'مصطفى','Faris':'فارس',
    'Zainab':'زينب','Khadija':'خديجة','Nayla':'نايلة','Hira':'هيرا','Sana':'سناء','Sadia':'صادية',
    'Mehek':'مهك','Anaya':'أنايا','Aliya':'عالية','Priya':'بريا','Anika':'أنيكة','Diya':'ديا',
    'Riya':'ريا','Saanvi':'سانفي','Anvi':'أنفي','Sofia':'صوفيا','Maya':'مايا','Nour':'نور',
    'Zoe':'زوي','Sophia':'سوفيا','Olivia':'أوليفيا','Emma':'إيما',
}
AR_LAST = {
    'Al-Zahrani':'الزهراني','Al-Qahtani':'القحطاني','Al-Shehri':'الشهري','Al-Ghamdi':'الغامدي',
    'Al-Maliki':'المالكي','Al-Dosari':'الدوسري','Al-Harbi':'الحربي','Al-Otaibi':'العتيبي',
    'Al-Sulami':'السلمي','Al-Rashid':'الراشد','Al-Anazi':'العنزي','Al-Mutairi':'المطيري',
    'Al-Fayez':'الفايز','Al-Sudais':'السديس','Al-Saud':'آل سعود','Al-Hashemi':'الهاشمي',
    'Al-Tamimi':'التميمي','Al-Hussein':'الحسين','Al-Yamani':'اليماني','Al-Sabah':'الصباح',
    'Ahmed':'أحمد','Ali':'علي','Hassan':'حسن','Hussain':'حسين','Malik':'مالك','Sheikh':'شيخ',
    'Siddiqui':'صديقي','Shaikh':'شيخ','Rahman':'رحمن','Mahmood':'محمود','Sharma':'شارما',
    'Patel':'باتل','Gupta':'جوبتا','Singh':'سينغ','Kumar':'كومار','Reddy':'ريدي','Ibrahim':'إبراهيم',
    'Mansoor':'منصور','Saleh':'صالح','Habib':'حبيب','Chen':'تشين','Wang':'وانج','Garcia':'جارسيا',
    'Kim':'كيم','Smith':'سميث','Brown':'براون','Khan':'خان',
}

EXPAT_COUNTRIES = ['Pakistan','India','Egypt','Yemen','Jordan','Syria','Sudan','Bangladesh',
                   'Philippines','Indonesia','United Kingdom','United States']
RELIGIONS = ['Muslim']*8 + ['Non-Muslim']*2
ENROLLMENT = ['New Student']*3 + ['Regular (Continuing)']*5 + ['Transfer']*2
FEE_CAT_MAP = {'New Student':'New','Regular (Continuing)':'Regular','Transfer':'Transfer'}
ADM_DATES = [date(2022,9,1), date(2023,9,1), date(2024,9,1), date(2025,9,1)]


def dob_for_grade(grade_name):
    m = re.search(r'(\d+)', grade_name or '')
    if m:
        age = int(m.group(1)) + 5
    elif 'KG' in grade_name:
        age = 4
    elif 'Pre' in grade_name:
        age = 4
    elif 'Nursery' in grade_name:
        age = 3
    elif 'Reception' in grade_name or 'Kinder' in grade_name:
        age = 5
    else:
        age = 8
    today = date.today()
    yr = today.year - age
    return date(yr, random.randint(1,12), random.randint(1,28))


def saudi_id():    return '1' + ''.join(str(random.randint(0,9)) for _ in range(9))
def iqama_id():    return '2' + ''.join(str(random.randint(0,9)) for _ in range(9))
def passport_id(): return ''.join(random.choices('ABCDEFGHJKLMN', k=2)) + ''.join(str(random.randint(0,9)) for _ in range(7))
def phone_num():   return '+9665' + ''.join(str(random.randint(0,9)) for _ in range(8))


academic_year = AcademicYear.objects.filter(is_current=True).first() or AcademicYear.objects.first()
ACADEMIC_NAME = academic_year.name
STUDY_MODES = list(StudyMode.objects.filter(is_active=True).values_list('name', flat=True))

rows = []
for division in Division.objects.filter(is_active=True):
    grades = list(Grade.objects.filter(division=division).order_by('order', 'name'))
    if not grades:
        print(f"Skipping {division.name} — no grades.")
        continue
    grade_sections = {g.id: list(Section.objects.filter(grade=g)) for g in grades}

    div_count = 0
    for n in range(1, 1001):
        grade = grades[n % len(grades)]
        secs  = grade_sections.get(grade.id) or []
        if not secs:
            continue
        section = secs[n % len(secs)]

        is_saudi = random.random() < 0.55
        gender   = random.choice(['Male', 'Female'])

        if is_saudi:
            first = random.choice(SAUDI_M if gender == 'Male' else SAUDI_F)
            last  = random.choice(LASTNAMES)
            nationality = 'Saudi Arabia'
            id_type = 'National ID'
            nat_id, iqama, passport = saudi_id(), '', ''
            birth_place = random.choice(['Riyadh','Jeddah','Mecca','Madinah','Dammam','Khobar','Tabuk','Buraidah','Abha'])
        else:
            first = random.choice(EXPAT_M if gender == 'Male' else EXPAT_F)
            last  = random.choice(EXPAT_LAST)
            nationality = random.choice(EXPAT_COUNTRIES)
            if random.random() < 0.7:
                id_type, nat_id, iqama, passport = 'Iqama', '', iqama_id(), ''
            else:
                id_type, nat_id, iqama, passport = 'Passport', '', '', passport_id()
            birth_place = random.choice(['Karachi','Mumbai','Cairo','Sanaa','Amman','Damascus','Khartoum','Dhaka','Manila','Jakarta','London','New York'])

        full_name   = f"{first} {last}"
        arabic_name = f"{AR_FIRST.get(first, first)} {AR_LAST.get(last, last)}"

        father_first = random.choice(SAUDI_M if is_saudi else EXPAT_M)
        mother_first = random.choice(SAUDI_F if is_saudi else EXPAT_F)
        father_name  = f"{father_first} {last}"
        mother_name  = f"{mother_first} {last}"

        enrollment   = random.choice(ENROLLMENT)
        fee_category = FEE_CAT_MAP.get(enrollment, 'Regular')
        study_mode   = random.choice(STUDY_MODES) if STUDY_MODES else ''
        admission    = random.choice(ADM_DATES)
        religion     = random.choice(RELIGIONS)

        rows.append([
            '',                                   # Student ID (blank → auto)
            full_name, arabic_name,
            gender,
            dob_for_grade(grade.name).isoformat(),
            nationality, id_type,
            nat_id, iqama, passport,
            religion, birth_place,
            division.name, grade.name, section.name, ACADEMIC_NAME, str(n).zfill(3),
            enrollment, study_mode, fee_category,
            admission.isoformat(), 'Yes',
            father_name, mother_name,
            phone_num(),
            f"{first.lower()}.{last.lower().replace('-','')}{n}@parent.com",
            f"{random.randint(1,300)} Al-Nuzha Street, Jeddah",
        ])
        div_count += 1
    print(f"  {division.name}: {div_count} rows")

HEADERS = [
    'Student ID','Full Name','Arabic Name','Gender','Date of Birth',
    'Nationality','ID Type','National ID','Iqama Number','Passport Number',
    'Religion','Birth Place',
    'Division','Grade','Section','Academic Year','Roll No.',
    'Enrollment Type','Study Mode','Fee Category','Admission Date','Active',
    'Father Name','Mother Name','Guardian Phone','Guardian Email','Address',
]

with open(OUT, 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(HEADERS)
    w.writerows(rows)

print(f"OK - wrote {len(rows)} rows to {OUT}")
