import typer

from single_custodian_rule import send_lambda_request, build_all_cloudcustodian_rules
from validate_custodian_rules import custodian_validate_one, custodian_validate_all
#from build_custodian_rules import build_all_cloudcustodian_rules

app = typer.Typer()



@app.command()
def validate(scan_yml: str):
    custodian_validate_one(scan_yml)

@app.command()
def validate_all():
    custodian_validate_all()

@app.command()
def run_lambda(scan_yml: str):
    send_lambda_request(scan_yml)

@app.command()
def create_artifacts():
    build_all_cloudcustodian_rules()



if __name__ == "__main__":
    app()