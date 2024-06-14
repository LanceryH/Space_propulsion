# Started the 14/06/2024 21:00 by Hugo Lancery
# This file contains all the necessary functions

from pydantic import BaseModel
import numpy as np
from dataclasses import dataclass

@dataclass
class Propulsion():
    R: float = 8.31446261815324 # Perfect gaz constant -> [J/mol/K]

    def get_mass(self, M_0: float , Delta_V: float, ISP: float, g_0: float) -> float:
        """
        This functions return  the ΔM of propellant
        
        ΔM -> [kg] : Total mass consumed
        M0 -> [kg] : Initial mass launch
        ΔV -> [m/s] : Speed increment
        ISP -> [s] : Specific impulsion
        g0 -> [m/s²] : Gravity acceleration
        """
        return M_0*(1-np.exp(-Delta_V/(g_0*ISP)))

    def get_isp(self, F: float=None, m_dot: float=None, g_0: float=None, C_star: float=None, C_f: float=None) -> float:
        """
        This functions return  the ISP specific impulsion
        
        ISP -> [s] : Specific impulsion
        g0 -> [m/s²] : Gravity acceleration
        m_dot -> [kg/s] : Mass flow rate
        
        C* -> [m/s] : Characteristic speed
        Cf -> [ ] : Thrust coefficient
        """
        try:
            ISP = F/(g_0*m_dot)
            if ISP != None:
                return ISP
            ISP = C_star*C_f/g_0
            if ISP != None:
                return ISP
        except:
            print("Parameter error")

    def get_chimical_thrust(self, m_dot: float, V_s: float, A_s: float, P_s: float, P_inf: float) -> float:
        """
        This functions return  the chimical propulsion thrust
        
        m_dot -> [kg/s] : Mass flow rate
        V_s -> [m/s] : Ejection speed
        A_s -> [m²] : Nozzle exit area
        P_s -> [Pa] : Exit pressure
        P∝ -> [Pa] : External pressure
        """
        return m_dot*V_s+A_s*(P_s-P_inf)

    def get_charac_speed(self, gamma: float, T: float, M: float) -> float:
        """
        This functions return  the chimical propulsion thrust
        
        C* -> [m/s] : Characteristic speed
        γ -> [ ] : coefficient isentropic expansion 
        T -> [K] : Temperature
        M -> [kg/mol] : Mean molecular mass
        """
        return np.sqrt(gamma*T*(self.R/M))/(gamma*np.sqrt((2/(gamma+1))*(gamma+1)/(gamma-1)))

    def get_thrust_coef(self, gamma: float, P_s: float, P_c: float, A_s: float, A_c: float) -> float:
        """
        This functions return  the characteristic thrust
        
        Cf -> [ ] : Characteristic speed
        γ -> [ ] : coefficient isentropic expansion
        A_s -> [m²] : Nozzle exit area
        P_s -> [Pa] : Nozzle collar pressure
        A_c -> [m²] : Nozzle exit area
        P_c -> [Pa] : Nozzle collar pressure
        """
        return gamma*np.sqrt((2/(gamma-1))*(2/(gamma+1))*((gamma+1)/(gamma-1))*(1-(P_s/P_c))*(gamma-1)/gamma)+(P_s/P_c)*(A_s/A_c)