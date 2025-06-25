import requests
from datetime import date
from typing import List, Dict, Union, Optional


def get_url(year: int) -> str:
    """Genera la URL para obtener los feriados de un año específico.
    
    Args:
        year: Año del cual se quieren obtener los feriados.
        
    Returns:
        URL completa para la API de feriados.
    """
    return f"https://nolaborables.com.ar/api/v2/feriados/{year}"


months = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
]
days = [
    'Lunes', 'Martes', 'Miércoles', 'Jueves',
    'Viernes', 'Sábado', 'Domingo'
]


def day_of_week(day: int, month: int, year: int) -> str:
    """Obtiene el día de la semana para una fecha específica.
    
    Args:
        day: Día del mes.
        month: Mes (1-12).
        year: Año.
        
    Returns:
        Nombre del día de la semana.
    """
    return days[date(year, month, day).weekday()]


class NextHoliday:
    """Clase para manejar la información del próximo feriado."""
    
    def __init__(self) -> None:
        """Inicializa la clase con valores por defecto."""
        self.loading = True
        self.year = date.today().year
        self.holiday = None

    def set_next(self, holidays: List[Dict[str, Union[int, str]]]) -> None:
        """Establece el próximo feriado a partir de una lista de feriados.
        
        Args:
            holidays: Lista de feriados obtenidos de la API.
        """
        now = date.today()
        today = {
            'day': now.day,
            'month': now.month
        }
        # Buscamos el proximo feriado (desde la fecha actual) valido
        holiday = next((h for h in holidays
                        if ((h['mes'] == today['month'] and
                             h['dia'] > today['day'])or
                             h['mes'] > today['month'])), holidays[0])
        self.loading = False
        self.holiday = holiday

    def fetch_holidays(self) -> None:
        """Obtiene los feriados del año actual desde la API."""
        response = requests.get(get_url(self.year))
        data = response.json()
        self.set_next(data)

    def next_holidays_byType(self, tipo: str) -> Union[Dict[str, Union[int, str]], List]:
        """Obtiene el próximo feriado de un tipo específico.
        
        Args:
            tipo: Tipo de feriado a buscar.
            
        Returns:
            Datos del feriado encontrado o lista vacía si no hay.
        """
        response = requests.get(get_url(self.year))
        holidays = response.json()
        now = date.today()
        today = {
            'day': now.day,
            'month': now.month
        }
        # Buscamos el proximo feriado (desde la fecha actual) valido tanto por fecha como por el tipo solicitado
        holiday = [
            h for h in holidays
            if ((h['mes'] == today['month'] and h['dia'] > today['day']) or
                h['mes'] > today['month']) and (h['tipo'] == tipo)
        ]
        return holiday[0] if holiday else []

    def string_holiday(self) -> str:
        """Genera una cadena con la fecha formateada del próximo feriado.
        
        Returns:
            Fecha del feriado en formato legible.
        """
        return (f"{day_of_week(self.holiday['dia'], self.holiday['mes'], self.year)} "
                f"{self.holiday['dia']} de {months[self.holiday['mes'] - 1]} del "
                f"{self.year}")

    def string_motivo(self) -> str:
        """Obtiene el motivo del próximo feriado.
        
        Returns:
            Motivo del feriado.
        """
        return str(self.holiday['motivo'])

    def render(self) -> None:
        """Muestra por consola la información del próximo feriado."""
        if self.loading:
            print("Buscando...")
        else:
            print("Próximo feriado")
            print(self.holiday['motivo'])
            print("Fecha:")
            print(day_of_week(self.holiday['dia'], self.holiday['mes'], self.year))
            print(self.holiday['dia'])
            print(months[self.holiday['mes'] - 1])
            print("Tipo:")
            print(self.holiday['tipo'])


next_holiday: NextHoliday = NextHoliday()
next_holiday.fetch_holidays()
next_holiday.render()