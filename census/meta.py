# -*- coding: utf-8 -*-

cols_desc = (
    # CODE              description   # rank
    ('AGE',             'age'),  # 0
    ('WORKER',          'class of worker'),  # 1
    ('INDUS_RECODE',    'detailed industry recode'),  # 2
    ('OCCUP_RECODE',    'detailed occupation recode'),  # 3
    ('EDU',             'education'),  # 4
    ('WPERH',           'wage per hour'),  # 5
    ('EDULW',           'enroll in edu inst last wk'),  # 6
    ('MARIT',           'marital stat'),  # 7
    ('INDUS_CODE',      'major industry code'),  # 8
    ('OCCUP_CODE',      'major occupation code'),  # 9
    ('RACE',            'race'),  # 10
    ('HISP',            'hispanic origin'),  # 11
    ('SEX',             'sex'),  # 12
    ('LAB_UNION',       'member of a labor union'),  # 13
    ('UNEMP_REASON',    'reason for unemployment'),  # 14
    ('WORK_TIME',       'full or part time employment stat'),  # 15
    ('CAP_GAINS',       'capital gains'),  # 16
    ('CAP_LOSSES',      'capital losses'),  # 17
    ('STOCK_DIV',       'dividends from stocks'),  # 18
    ('TAX_FILER',       'tax filer stat'),  # 19
    ('RESI_REGION',     'region of previous residence'),  # 20
    ('RESI_PREV',       'state of previous residence'),  # 21
    ('FAMILY_STAT',     'detailed household and family stat'),  # 22
    ('FAMILY_SUM',      'detailed household summary in household'),  # 23
    ('INSTANCE_WEIGHT', 'instance weight'),  # 24
    ('MIG_MSA',         'migration code-change in msa'),  # 25
    ('MIG_REGION',      'migration code-change in reg'),  # 26
    ('MIG_MOVE',        'migration code-move within reg'),  # 27
    ('RESI_1YEAR',      'live in this house 1 year ago'),  # 28
    ('MIG_SUNBELT',     'migration prev res in sunbelt'),  # 29
    ('EMPLOYEES_NB',    'num persons worked for employer'),  # 30
    ('UNDER_18_NB',     'family members under 18'),  # 31
    ('ORIG_FATHER',     'country of birth father'),  # 32
    ('ORIG_MOTHER',     'country of birth mother'),  # 33
    ('ORIG_SELF',       'country of birth self'),  # 34
    ('CITIZEN',         'citizenship'),  # 35
    ('SELF_EMPLOYED',   'own business or self employed'),  # 36
    ('VETERAN_Q',       'fill inc questionnaire for veteran\'s admin'),  # 37
    ('VETERAN_BEN',     'veterans benefits'),  # 38
    ('WWORKY',          'weeks worked in year'),  # 39
    ('YEAR',            'year'),  # 40
    ('TARGET',          'yearly income'),  # 41
)

if __name__ == '__main__':
    print cols_desc
