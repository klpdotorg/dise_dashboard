# from django.db import models


def search_choices(t, value):
    """
    looks for index in a tuple of tuples

    >>> search_choices(YESNO, 'Yes')
    1

    """
    for k, v in t:
        if v == value:
            return k
    return False


def search_choices_by_key(t, key):
    """
    looks for index in a tuple of tuples

    >>> search_choices(YESNO, 'Yes')
    1

    """
    for k, v in t:
        if k == key:
            return v
    return False


YESNO = (
    (0, 'Not Applicable'),
    (1, 'Yes'),
    (2, 'No'),
    (3, 'Yes but not functional'),
    (4, 'Unknown')
)

AREA = (
    (1, 'Rural'),
    (2, 'Urban'),
)

SCHOOL_CATEGORY = (
    (1, "Primary only (1-5)"),
    (2, "Primary With Upper Primary(1-8)"),
    (3, "Primary with Upper Primary and Secondary and higher Secondary(1-12)"),
    (4, "Upper Primary only(6-8)"),
    (5, "Upper Primary with Secondary and higher Secondary(6-12)"),
    (6, "Primary, with Upper Primary and Secondary(1-10)"),
    (7, "Upper Primary with Secondary(6-10)"),
    (8, "Secondary only(9 & 10)"),
    (10, "Secondary with Hr. Secondary(9-12) "),
    (11, "Hr. Secondary only/Jr. College(11 & 12)")
)

SCHOOL_MANAGEMENT = (
    (1, "Department of Education"),
    (2, "Tribal/Social Welfare Department"),
    (3, "Local body"),
    (4, "Pvt. Aided"),
    (5, "Pvt. Unaided"),
    (6, "Others"),
    (7, "Central Govt."),
    (8, "Unrecognised"),
    (97, "Madarsa recognized (by Wakf board/Madarsa Board)"),
    (98, "Madarsa unrecognized")
)

SCHOOL_TYPES = (
    (1, 'Boys'),
    (2, 'Girls'),
    (3, 'Co-educational')
)

MEDIUM = (
    (1, "Assamese"),
    (2, "Bengali"),
    (3, "Gujarati"),
    (4, "Hindi"),
    (5, "Kannada"),
    (6, "Kashmiri"),
    (7, "Konkani"),
    (8, "Malayalam"),
    (9, "Manipuri"),
    (10, "Marathi"),
    (11, "Nepali"),
    (12, "Odia"),
    (13, "Punjabi"),
    (14, "Sanskrit"),
    (15, "Sindhi"),
    (16, "Tamil"),
    (17, "Telugu"),
    (18, "Urdu"),
    (19, "English"),
    (20, "Bodo"),
    (21, "Mising"),
    (22, "Dogri"),
    (23, "Khasi"),
    (24, "Garo"),
    (25, "Mizo"),
    (26, "Bhutia"),
    (27, "Lepcha"),
    (28, "Limboo"),
    (29, "French"),
    (99, "Others")
)

MDM_STATUS = (
    (0, 'Not applicable'),
    (1, 'Not provided'),
    (2, 'Provided & prepared in school premises'),
    (3, 'Provided but not prepared in school premises'),
    (4, 'Unknown'),
    (9, 'Unknown')
)

KITCHENSHED_STATUS = (
    (0, 'not applicable'),
    (1, 'available'),
    (2, 'not available'),
    (3, 'Under construction'),
    (4, 'classroom used as kitchen'),
)

BOUNDARY_WALL = (
    (0, "Not Applicable"),
    (1, "Pucca"),
    (2, "Pucca but broken"),
    (3, "Barbed wire fencing"),
    (4, "Hedges"),
    (5, "No boundary wall"),
    (6, "Others"),
    (7, "Partial"),
    (8, "Under Construction"),
    (9, "Unknown"),
    (10, "Unknown"),
)

BUILDING_STATUS = (
    (1, "Private "),
    (2, "Rented"),
    (3, "Government"),
    (4, "Government school in a rent free building"),
    (5, "No Building"),
    (6, "Dilapidated"),
    (7, "Under Construction"),
    (9, "Unknown"),
)
