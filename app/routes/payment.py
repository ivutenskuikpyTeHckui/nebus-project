from fastapi import APIRouter

from app.controllers.payment import create_payment, get_payment
from app.models.response_models.payment import (
    CreatePaymentResponseModel,
    PaymentResponseModel,
)

router = APIRouter()
router.add_api_route(
    "",
    create_payment,
    methods=["POST"],
    status_code=202,
    response_model=CreatePaymentResponseModel,
)
router.add_api_route(
    "/{payment_id}",
    get_payment,
    methods=["GET"],
    response_model=PaymentResponseModel,
    response_model_by_alias=True,
)
