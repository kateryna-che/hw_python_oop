from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, List, Type

SWM: str = 'SWM'
RUN: str = 'RUN'
WLK: str = 'WLK'


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    TEXT: ClassVar[str] = ('Тип тренировки: {training_type}; '
                           'Длительность: {duration:.3f} ч.; '
                           'Дистанция: {distance:.3f} км; '
                           'Ср. скорость: {speed:.3f} км/ч; '
                           'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.TEXT.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MINUTES_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    RUN_COEFF_CAL_1: int = 18
    RUN_COEFF_CAL_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.RUN_COEFF_CAL_1 * self.get_mean_speed()
                 - self.RUN_COEFF_CAL_2)
                * self.weight / self.M_IN_KM
                * self.duration * self.MINUTES_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WLK_COEFF_CAL_1: float = 0.035
    WLK_COEFF_CAL_2: int = 2
    WLK_COEFF_CAL_3: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.WLK_COEFF_CAL_1 * self.weight
                 + (self.get_mean_speed() ** self.WLK_COEFF_CAL_2
                    // self.height) * self.WLK_COEFF_CAL_3 * self.weight)
                * self.duration * self.MINUTES_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SWM_COEFF_CAL_1: float = 1.1
    SWM_COEFF_CAL_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.SWM_COEFF_CAL_1)
                * self.SWM_COEFF_CAL_2 * self.weight)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_types: Dict[str, Type[Training]] = {SWM: Swimming,
                                                RUN: Running,
                                                WLK: SportsWalking}
    if workout_type in workout_types:
        return workout_types[workout_type](*data)
    raise ValueError('Тип тренировки не предусмотрен')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        (SWM, [720, 1, 80, 25, 40]),
        (RUN, [15000, 1, 75]),
        (WLK, [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
