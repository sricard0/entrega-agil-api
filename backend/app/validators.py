import re

def sanitize_document(value: str) -> str:
    """Remove tudo que não for dígito."""
    return re.sub(r"\D", "", value or "")


def is_valid_cpf(cpf: str) -> bool:
    cpf = sanitize_document(cpf)
    if len(cpf) != 11:
        return False
    if cpf == cpf[0] * 11:
        return False

    # 1º dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    dv1 = 0 if resto == 10 else resto
    if dv1 != int(cpf[9]):
        return False

    # 2º dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    dv2 = 0 if resto == 10 else resto
    if dv2 != int(cpf[10]):
        return False

    return True


def is_valid_cnpj(cnpj: str) -> bool:
    cnpj = sanitize_document(cnpj)
    if len(cnpj) != 14:
        return False
    if cnpj == cnpj[0] * 14:
        return False

    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj[i]) * pesos1[i] for i in range(12))
    resto = soma % 11
    dv1 = 0 if resto < 2 else 11 - resto
    if dv1 != int(cnpj[12]):
        return False

    pesos2 = [6] + pesos1
    soma = sum(int(cnpj[i]) * pesos2[i] for i in range(13))
    resto = soma % 11
    dv2 = 0 if resto < 2 else 11 - resto
    if dv2 != int(cnpj[13]):
        return False

    return True
