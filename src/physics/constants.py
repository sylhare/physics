"""Physical constants and planetary data."""

from dataclasses import dataclass

# Gravitational constant (m³ kg⁻¹ s⁻²)
G = 6.67430e-11

# Solar mass (kg)
M_SUN = 1.989e30

# Astronomical Unit (m)
AU = 1.496e11


@dataclass
class PlanetData:
    """Orbital data for a planet."""

    name: str
    semi_major_axis_au: float  # Semi-major axis in AU
    orbital_period_years: float  # Orbital period in Earth years
    eccentricity: float  # Orbital eccentricity


# Planetary data (Mercury through Saturn, as in Feynman's lecture)
PLANETS: dict[str, PlanetData] = {
    "Mercury": PlanetData(
        name="Mercury",
        semi_major_axis_au=0.387,
        orbital_period_years=0.241,
        eccentricity=0.206,
    ),
    "Venus": PlanetData(
        name="Venus",
        semi_major_axis_au=0.723,
        orbital_period_years=0.615,
        eccentricity=0.007,
    ),
    "Earth": PlanetData(
        name="Earth",
        semi_major_axis_au=1.000,
        orbital_period_years=1.000,
        eccentricity=0.017,
    ),
    "Mars": PlanetData(
        name="Mars",
        semi_major_axis_au=1.524,
        orbital_period_years=1.881,
        eccentricity=0.093,
    ),
    "Jupiter": PlanetData(
        name="Jupiter",
        semi_major_axis_au=5.203,
        orbital_period_years=11.86,
        eccentricity=0.048,
    ),
    "Saturn": PlanetData(
        name="Saturn",
        semi_major_axis_au=9.537,
        orbital_period_years=29.46,
        eccentricity=0.054,
    ),
}
