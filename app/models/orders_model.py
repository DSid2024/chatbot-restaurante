from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class OrderModel(BaseModel):
    tipo: str = Field(
        ...,
        description="Tipo do pedido ('delivery' ou 'local')",
        json_schema_extra={"example": "delivery"}
    )
    itens: List[int] = Field(
        ...,
        description="Lista de códigos de itens",
        json_schema_extra={"example": [1, 2, 3]}
    )
    endereco: Optional[str] = Field(
        None,
        description="Endereço para entrega, obrigatório se tipo=delivery",
        json_schema_extra={"example": "Rua Exemplo, 123"}
    )

    @field_validator('tipo')
    def tipo_must_be_valid(cls, v):
        if v not in ['delivery', 'local']:
            raise ValueError("Tipo inválido. Use 'delivery' ou 'local'.")
        return v

    @field_validator('endereco')
    def endereco_required_if_delivery(cls, v, values):
        tipo = values.data.get('tipo')  # Use `values.data` para acessar os valores validados
        if tipo == 'delivery' and not v:
            raise ValueError("Endereço é obrigatório para pedidos do tipo 'delivery'.")
        return v

