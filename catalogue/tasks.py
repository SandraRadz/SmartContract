from catalogue.models import Product, PurchaseStatus
from contracts_api import ContractWrapper
from smartcontract.settings import INFURA_KEY
from smartcontract import celery_app


@celery_app.task
def submit_new_smart_contract(seller_hash, solver_hash, buyer_private_key, price, product_id):
    wrapper = ContractWrapper(INFURA_KEY, buyer_private_key, timeout=600)  # default timeout value is 600

    seller_address = seller_hash
    solver_address = solver_hash

    product_obj = Product.objects.get(id=product_id)

    result = wrapper.create(
        seller_address,  # str
        solver_address,  # str
        int(float(price)),  # price of the product: should be int
        str(product_id)  # product id: should be int casted to string
    )
    product_obj.contract_address = result["receipt"]["contractAddress"]
    product_obj.status = PurchaseStatus.ORDER
    product_obj.save()


@celery_app.task
def send_product(solver_private_hash, contract_address, product_id):
    wrapper = ContractWrapper(INFURA_KEY, solver_private_hash, timeout=600)  # default timeout value is 600
    product_obj = Product.objects.get(id=product_id)

    result = wrapper.send(
        contract_address,  # smart contract address: str
    )
    product_obj.status = PurchaseStatus.SENT
    product_obj.save()


@celery_app.task
def receive_product(buyer_private_hash, contract_address, product_id):
    wrapper = ContractWrapper(INFURA_KEY, buyer_private_hash, timeout=600)  # default timeout value is 600
    product_obj = Product.objects.get(id=product_id)

    wrapper.confirm(
        contract_address,  # smart contract address: str
    )
    product_obj.status = PurchaseStatus.RECEIVED
    product_obj.save()


@celery_app.task
def refund(solver_private_hash, contract_address, product_id):
    wrapper = ContractWrapper(INFURA_KEY, solver_private_hash, timeout=600)  # default timeout value is 600
    product_obj = Product.objects.get(id=product_id)

    wrapper.build(
        contract_address,  # smart contract address: str,
        'refund'
    )
    product_obj.status = PurchaseStatus.REFUND_BY_SOLVER
    product_obj.save()


@celery_app.task
def no_refund(solver_private_hash, contract_address, product_id):
    wrapper = ContractWrapper(INFURA_KEY, solver_private_hash, timeout=600)  # default timeout value is 600
    product_obj = Product.objects.get(id=product_id)

    wrapper.build(
        contract_address,  # smart contract address: str
        'no_refund'
    )
    product_obj.status = PurchaseStatus.NO_REFUND_BY_SOLVER
    product_obj.save()


@celery_app.task
def problem(buyer_private_hash, contract_address, product_id):
    wrapper = ContractWrapper(INFURA_KEY, buyer_private_hash, timeout=600)  # default timeout value is 600
    product_obj = Product.objects.get(id=product_id)

    wrapper.build(
        contract_address,  # smart contract address: str
        'problem', 'description'
    )
    product_obj.status = PurchaseStatus.PROBLEM
    product_obj.save()