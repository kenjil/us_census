# -*- coding: utf-8 -*-

cols = (
    # CODE              # rank
    'AGE',              # 0
    'WORKER',           # 1
    'INDUS_D_CODE',     # 2
    'OCCUP_D_CODE',     # 3
    'EDU',              # 4
    'WPERH',            # 5
    'EDULW',            # 6
    'MARIT',            # 7
    'INDUS_M_CODE',       # 8
    'OCCUP_M_CODE',       # 9
    'RACE',             # 10
    'HISP',             # 11
    'SEX',              # 12
    'LAB_UNION',        # 13
    'UNEMP_REASON',     # 14
    'WORK_TIME',        # 15
    'CAP_GAINS',        # 16
    'CAP_LOSSES',       # 17
    'STOCK_DIV',        # 18
    'TAX_FILER',        # 19
    'RESI_REGION',      # 20
    'RESI_PREV',        # 21
    'FAMILY_STAT',      # 22
    'FAMILY_SUM',       # 23
    'INSTANCE_WEIGHT',  # 24
    'MIG_MSA',          # 25
    'MIG_REGION',       # 26
    'MIG_MOVE',         # 27
    'RESI_1YEAR',       # 28
    'MIG_SUNBELT',      # 29
    'EMPLOYEES_NB',     # 30
    'UNDER_18_NB',      # 31
    'ORIG_FATHER',      # 32
    'ORIG_MOTHER',      # 33
    'ORIG_SELF',        # 34
    'CITIZEN',          # 35
    'SELF_EMPLOYED',    # 36
    'VETERAN_Q',        # 37
    'VETERAN_BEN',      # 38
    'WWORKY',           # 39
    'YEAR',             # 40
    'TARGET',           # 41
)

cols_desc = {
    # CODE              description
    'AGE':             'age',
    'WORKER':          'class of worker',
    'INDUS_D_CODE':    'detailed industry recode',
    'OCCUP_D_CODE':    'detailed occupation recode',
    'EDU':             'education',
    'WPERH':           'wage per hour',
    'EDULW':           'enroll in edu inst last wk',
    'MARIT':           'marital stat',
    'INDUS_M_CODE':      'major industry code',
    'OCCUP_M_CODE':      'major occupation code',
    'RACE':            'race',
    'HISP':            'hispanic origin',
    'SEX':             'sex',
    'LAB_UNION':       'member of a labor union',
    'UNEMP_REASON':    'reason for unemployment',
    'WORK_TIME':       'full or part time employment stat',
    'CAP_GAINS':       'capital gains',
    'CAP_LOSSES':      'capital losses',
    'STOCK_DIV':       'dividends from stocks',
    'TAX_FILER':       'tax filer stat',
    'RESI_REGION':     'region of previous residence',
    'RESI_PREV':       'state of previous residence',
    'FAMILY_STAT':     'detailed household and family stat',
    'FAMILY_SUM':      'detailed household summary in household',
    'INSTANCE_WEIGHT': 'instance weight',
    'MIG_MSA':         'migration code-change in msa',
    'MIG_REGION':      'migration code-change in reg',
    'MIG_MOVE':        'migration code-move within reg',
    'RESI_1YEAR':      'live in this house 1 year ago',
    'MIG_SUNBELT':     'migration prev res in sunbelt',
    'EMPLOYEES_NB':    'num persons worked for employer',
    'UNDER_18_NB':     'family members under 18',
    'ORIG_FATHER':     'country of birth father',
    'ORIG_MOTHER':     'country of birth mother',
    'ORIG_SELF':       'country of birth self',
    'CITIZEN':         'citizenship',
    'SELF_EMPLOYED':   'own business or self employed',
    'VETERAN_Q':       'fill inc questionnaire for veteran\'s admin',
    'VETERAN_BEN':     'veterans benefits',
    'WWORKY':          'weeks worked in year',
    'YEAR':            'year',
    'TARGET':          'yearly income',
}
