import utils

from elg import FlaskService
from elg.model import Failure
from elg.model import TextRequest, AnnotationsResponse
from elg.model.base import StandardMessages


class NBNer(FlaskService):
    def process_single_text(self, text):
        """Single text handler that catches too large request and
        internal exception while parsing text"""
        if utils.is_exceed_limit(text):
            err_msg = "Submitted text has exceeded 512 tokens limit"
            tooLargeTextMessage = StandardMessages.\
                generate_elg_request_too_large(params=[err_msg])
            return Failure(errors=[tooLargeTextMessage])
        try:
            res = utils.ner_func(text)
        except Exception as err:
            internalErrorMessage = StandardMessages.\
                    generate_elg_service_internalerror(
                        params=[str(err)])
            return Failure(errors=[internalErrorMessage])
        return AnnotationsResponse(annotations=res)

    def process_text(self, request: TextRequest):
        text = request.content
        return self.process_single_text(text)


flask_service = NBNer("NB-ner")
app = flask_service.app
