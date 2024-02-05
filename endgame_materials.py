import math
from enum import Enum
from typing import Dict


class Material(str, Enum):
    Laser = "laser"
    SteelBar = "steel bar"
    FramedGlass = "framed glass"
    AdvancedCircuit = "advanced circuit"
    ElectricMotor = "electric motor"
    Radiator = "radiator"
    Glass = "glass"
    GoldBar = "gold bar"
    CopperWiring = "copper wiring"
    GoldWiring = "gold wiring"
    GoldFlakes = "gold flakes"
    Substrate = "substrate"
    BasicCircuit = "basic circuit"
    CopperBar = "copper bar"
    Plastic = "plastic"
    Epoxy = "epoxy"
    HeatSink = "heat sink"
    CopperPlate = "copper plate"
    Fiberglass = "fiberglass"
    def __repr__(self):return f"""\"{self.value}\""""
    def __str__(self):return self.value


base_materials = {
    Material.Glass,
    Material.GoldBar,
    Material.CopperBar,
    Material.SteelBar,
    Material.Plastic,
    Material.Epoxy,
}

# negative values are a quick and dirty hack to set locked values with no efficiency effect
# TODO: Update with a 'recipe' class and 'ingredient' class that properly set outputs and inputs, and which ones scale
recipes: Dict[Material, Dict[Material, float]] = {
    Material.Laser: {
        Material.GoldBar: -80,
        Material.SteelBar: -80,
        Material.FramedGlass: -80,
        Material.AdvancedCircuit: -40,
        Material.ElectricMotor: -2,
        Material.Radiator: -10,
    },
    Material.FramedGlass: {Material.Glass: 5, Material.SteelBar: 2},
    Material.AdvancedCircuit: {
        Material.CopperWiring: 4,
        Material.GoldWiring: 4,
        Material.GoldFlakes: 10,
        Material.Substrate: 2,
    },
    Material.ElectricMotor: {
        Material.BasicCircuit: 4,
        Material.CopperWiring: 10,
        Material.SteelBar: 8,
    },
    Material.Radiator: {Material.HeatSink: 4, Material.CopperWiring: 8},
    Material.CopperWiring: {Material.CopperBar: 4 / 2},  # 4in=2out
    Material.GoldWiring: {Material.GoldBar: 4 / 2},  # 4in=2out
    Material.Substrate: {Material.Fiberglass: 4, Material.Epoxy: 4},
    Material.GoldFlakes: {Material.GoldBar: 2 / 4},  # 2in=4out
    Material.BasicCircuit: {
        Material.CopperWiring: 6,
        Material.GoldFlakes: 10,
        Material.Substrate: 2,
    },
    Material.HeatSink: {Material.CopperPlate: 8, Material.CopperWiring: 6},
    Material.CopperPlate: {Material.CopperBar: 1},
    Material.Fiberglass: {Material.Glass: 2, Material.Plastic: 4},
}

for output, inputs in recipes.items():
    for input in inputs:
        # know how to make it
        if input in recipes:
            continue
        # tagged as baseline item
        if input in base_materials:
            continue
        print(f"Do not know how to make {input}")


def get_immediate_inputs(out_material: Material, out_qty: float, cost_reduction: float):
    actual_cost = 1 - cost_reduction
    inputs = {mat: in_qty for mat, in_qty in recipes[out_material].items()}
    # adjust prices ; negative values are locked and do not reduce with efficiency
    for m, q in inputs.items():
        if q < 0:
            inputs[m] = math.ceil(-q * out_qty)
        else:
            inputs[m] = math.ceil(q * out_qty * actual_cost)
    return inputs


def show_base_inputs(out_material: Material, out_qty: float, cost_reduction: float):
    # start with inputs to original material
    inputs = get_immediate_inputs(out_material, out_qty, cost_reduction)
    crafts: Dict[Material, int] = {}
    # loop until we get to base materials only
    while any(input not in base_materials for input in inputs):
        added_materials = {}
        handled_materials = set()
        for input, in_qty in inputs.items():
            # we do not dig into base materials they are an end point
            if input in base_materials: continue
            # break down the input to *its* inputs and their qty
            input_breakdown = get_immediate_inputs(input, in_qty, cost_reduction)
            for inner_material, inner_qty in input_breakdown.items():
                if inner_material in added_materials:
                    added_materials[inner_material] += inner_qty
                else:
                    added_materials[inner_material] = inner_qty
            handled_materials.add(input)
            # add this item as requiring crafting
            if input not in crafts:
                crafts[input] = 0
            crafts[input] += int(in_qty)
        # modify inputs now that we have finished the loop
        for handled_material in handled_materials:
            del inputs[handled_material]
        for added_material, added_qty in added_materials.items():
            if added_material in inputs:
                inputs[added_material] += added_qty
            else:
                inputs[added_material] = added_qty
    # no more non-base materials - we are done
    print("Requires these crafts...")
    for material, qty in crafts.items():
        print(f" - {qty}x {material}")
    print("Requires these base materials")
    for material, qty in inputs.items():
        print(f" - {qty}x {material}")


def get_discount(module_level: int):
    return {0: 0, 1: 0.1, 2: 0.25, 3: 0.4, 4: 0.45, 5: 0.5}[module_level]


# 4 lasers
show_base_inputs(Material.Laser, 4, get_discount(5))


# computer lab
show_base_inputs(Material.AdvancedCircuit, 100, get_discount(4))
