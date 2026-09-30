from ..domain.care_package_domain import CarePackage
from ..domain.care_package_errors import CarePackageValidationError


def validate_care_package(care_package: CarePackage) -> None:
    if care_package.min_age_days > care_package.max_age_days:
        raise CarePackageValidationError("min_age_days no puede ser mayor que max_age_days")
