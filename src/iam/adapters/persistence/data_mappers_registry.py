from abc import ABC, abstractmethod

from iam.adapters.persistence.data_mapper import DataMapper


class DataMappersRegistry(ABC):
    @abstractmethod
    def find_mapper[ModelT](self, model_type: type[ModelT]) -> DataMapper[ModelT]: ...
