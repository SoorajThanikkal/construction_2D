from django.shortcuts import render
from django.http import JsonResponse
import math

# Create your views here.

# from django.shortcuts import render
# from django.views import View
# from .models import Beam


# def get(self, request):
#         # Custom values
#     span = 5.0  # meters
#     live_load = 10.0  # kN/m
#     fck = 25  # N/mm²
#     fy = 500  # N/mm²

#         # Calculations
#     d = span / 12  # Effective depth
#     D = d + 0.05  # Overall depth (assuming 50mm cover)
#     b = max(0.3 * D, 0.2)  # Width, minimum 200mm
        
#     effective_span = min(span + d, span + b)
        
#     dead_load = b * D * 25  # kN/m (assuming 25 kN/m³ for reinforced concrete)
#     total_load = dead_load + live_load
#     factored_load = 1.5 * total_load
        
#     bending_moment = (factored_load * effective_span**2) / 8
        
#         # Simplified calculation for main reinforcement area (Ast)
#     xu_max = 0.48 * d
#     Mu_lim = 0.36 * xu_max / d * (1 - 0.42 * xu_max / d) * b * d**2 * fck
        
#     if bending_moment <= Mu_lim:
#             # Singly reinforced section
#         k = (fck / (fy * (1 - (fck / (fy * 1.15)))))
#         j = 1 - k / 3
#         Ast = (bending_moment * 1e6) / (fy * j * d)
#     else:
#             # Doubly reinforced section (simplified)
#         Ast = (0.5 * fck * b * d / fy) + (0.1 * b * d)  # Approximate calculation
        
#     shear_force = (factored_load * effective_span) / 2
#     nominal_shear_stress = shear_force * 1000 / (b * 1000 * d)  # N/mm²
        
#         # Create Beam object
#     beam = Beam(
#         span=span,
#         cover=50,
#         effective_depth=d * 1000,  # Convert to mm
#         overall_depth=D * 1000,  # Convert to mm
#         width=b * 1000,  # Convert to mm
#         effective_span=effective_span,
#         dead_load=dead_load,
#         live_load=live_load,
#         total_load=total_load,
#         factored_load=factored_load,
#         bending_moment=bending_moment,
#         limiting_moment=Mu_lim,
#         main_reinforcement_area=Ast,
#         shear_force=shear_force,
#         nominal_shear_stress=nominal_shear_stress
#     )
        
#     return render(request, 'beam_result.html', {'beam': beam})



import math
from django.shortcuts import render

def beam_design_view(request):
    # Given values from the image and cross-check with the design:
    span = 6.0# Span in meters
    s= span * 1000 #in mm
    d = 1/12 * s # Effective depth in mm
    cover = 40
    D = d + cover  # Overall depth including cover in mm  # Cover in mm
    b = 1/2 * D  # Width of the beam in mm
    fck = 20  # Concrete grade in MPa
    fy = 415  # Steel yield strength in MPa

    # Reinforcement details:
    main_bar_diameter = 20  # mm
    num_main_bars = 3  # Number of main bars
    stirrup_diameter = 8  # mm
    stirrup_spacing = 300  # mm center-to-center

    # Calculate area of reinforcement:
    Ast_provided = num_main_bars * (math.pi * (main_bar_diameter / 2) ** 2)  # mm²

    # Calculate dead load:
    unit_weight_RCC = 25  # kN/m³ (typical for reinforced concrete)
    DL = b / 1000 * D / 1000 * unit_weight_RCC  # Dead Load in kN/m

    # Assume imposed load (live load):
    imposed_load = 15.0  # kN/m² (assumed)

    # Total Load (W):
    W = DL + imposed_load  # kN/m

    # Factored Load (Wu):
    Wu = 1.5 * W  # kN/m

    # Bending Moment (Mu):
    Leff = span + d / 1000  # Effective span in meters
    Mu = (Wu * Leff ** 2) / 8  # kNm

    # Limiting Moment of Resistance:
    xu_max = 0.48 * d
    Mulim = 0.36 * fck * b * xu_max * (1 - 0.42 * xu_max / d) * (d / 1000) ** 2  # kNm

    # Check for depth:
    if Mu > Mulim:
        raise ValueError("Redesign required: Mu exceeds Mulim")

    # Shear Force (Vu):
    Vu = Wu * Leff / 2  # kN

    # Shear Capacity of Concrete (Vc):
    tau_c = 0.36  # MPa, design shear stress (assumed, varies with percentage of steel)
    Vc = tau_c * b * d / 1000  # kN

    # Check for shear reinforcement:
    shear_reinforcement = None
    if Vu > Vc:
        Av = (Vu - Vc) * 1000 / (0.87 * fy * stirrup_spacing)  # mm²/m
        shear_reinforcement = Av  # Provide shear reinforcement

    # Deflection check:
    span_to_depth_ratio = Leff / d
    permissible_ratio = 20  # Assumed value based on beam type, could be refined

    # Development Length (Ld):
    tau_bd = 1.2  # MPa, design bond stress (from IS 456:2000)
    Ld = (main_bar_diameter * fy) / (4 * tau_bd)  # mm

    # Minimum Reinforcement (As_min):
    As_min = 0.85 * (fck / fy) * b * d  # mm²

    # Maximum Reinforcement (As_max):
    As_max = 0.04 * b * d  # mm²

    # Context to pass to template:
    context = {
        'span': span * 1000,
        'load': W,
        'width': b,
        'depth': d,
        'overall_depth': D,
        'cover': cover,
        'reinforcement': Ast_provided,
        'num_bars': num_main_bars,
        'bar_diameter': main_bar_diameter,
        'stirrup_diameter': stirrup_diameter,
        'stirrup_spacing': stirrup_spacing,
        'Mu': Mu,
        'Mulim': Mulim,
        'Vu': Vu,
        'Vc': Vc,
        'shear_reinforcement': shear_reinforcement,
        'span_to_depth_ratio': span_to_depth_ratio,
        'permissible_ratio': permissible_ratio,
        'Ld': Ld,
        'As_min': As_min,
        'As_max': As_max,
    }

    return render(request, 'beam_result.html', context)




def index(request):
    return render(request, 'index.html')

