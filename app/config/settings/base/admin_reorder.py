# django-modeladmin-reorder
ADMIN_REORDER = (
    # 세미나
    {'app': 'seminars', 'label': '세미나', 'models': (
        {'model': 'seminars.Seminar', 'label': '세미나'},
        {'model': 'seminars.Track', 'label': '트랙'},
        {'model': 'seminars.Session', 'label': '세션'},
    )},
    {'app': 'seminars', 'label': '세미나 추가정보', 'models': (
        {'model': 'seminars.Speaker', 'label': '발표자'},
        {'model': 'seminars.SpeakerLinkType', 'label': '발표자 링크 유형'},
        {'model': 'seminars.SpeakerLink', 'label': '발표자 링크'},
        {'model': 'seminars.SessionVideo', 'label': '세션 영상'},
        {'model': 'seminars.SessionLink', 'label': '세션 링크'},
        {'model': 'seminars.SessionFile', 'label': '세션 첨부파일'},
    )},

    # 스폰서
    {'app': 'sponsors', 'label': '스폰서', 'models': (
        {'model': 'sponsors.SponsorTier', 'label': '스폰서 등급'},
        {'model': 'sponsors.Sponsor', 'label': '스폰서'},
    )},

    # 인증
    {'app': 'members', 'label': '인증 및 권한', 'models': (
        {'model': 'members.User', 'label': '사용자'},
        {'model': 'auth.Group', 'label': '그룹'},
        {'model': 'authtoken.Token', 'label': '인증토큰'},
        {'model': 'rest_framework_api_key.APIKey', 'label': 'APIKey'},
    )},
)
