from django.test import TestCase
from model_bakery import baker

from seminars.models import SessionVideo, Session


class SessionVideoModelTest(TestCase):
    def test_save(self):
        session = baker.make(Session)
        sv = SessionVideo(session=session, key="1", url="http://sample.com")
        self.assertRaises(ValueError, sv.save)

        sv = SessionVideo(
            session=session, type=SessionVideo.TYPE_YOUTUBE, url="http://sample.com"
        )
        self.assertRaises(ValueError, sv.save)

        sv = SessionVideo(
            session=session, type=SessionVideo.TYPE_LINK, url="http://sample.com"
        )
        sv.save()
