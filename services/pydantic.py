from flask import Response, abort, jsonify, make_response
from pydantic import BaseModel


class ResponseError(BaseModel):
    code: int
    message: str

    def make_response(self) -> Response:
        return make_response(jsonify(self.json()), self.code)

    def abort(self) -> None:
        """Raise error."""
        abort(self.make_response())
