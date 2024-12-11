from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class ReservationModel(BaseModel):
    # Data da reserva, deve ser uma string no formato 'dd/mm/yyyy'
    data: str = Field(
        ...,
        description="Data da reserva",
        json_schema_extra={"example": "10/12/2024"}
    )
    # Hora da reserva, deve ser uma string no formato 'hh:mm'
    hora: str = Field(
        ...,
        description="Hora da reserva",
        json_schema_extra={"example": "20:00"}
    )
    # Número de pessoas, deve ser maior que 0
    pessoas: int = Field(
        ...,
        gt=0,
        description="Número de pessoas na reserva",
        json_schema_extra={"example": 4}
    )

    @field_validator('data')
    def validate_data(cls, v):
        """
        Valida se a data está no formato correto ('dd/mm/yyyy') e se é uma data válida.
        """
        try:
            datetime.strptime(v, "%d/%m/%Y")
        except ValueError:
            raise ValueError("A data deve estar no formato 'dd/mm/yyyy' e ser válida.")
        return v

    @field_validator('hora')
    def validate_hora(cls, v):
        """
        Valida se a hora está no formato correto ('hh:mm') e se é uma hora válida.
        """
        try:
            datetime.strptime(v, "%H:%M")
        except ValueError:
            raise ValueError("A hora deve estar no formato 'hh:mm' e ser válida.")
        return v
