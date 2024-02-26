import torch
import taichi as ti
from coralai.substrate.substrate import Substrate
from coralai.instances.minimal.minimal_vis import MinimalVis
from coralai.instances.minimal.minimal_organism import MinimalOrganism

SHAPE = (400, 400)

def define_substrate(shape):
    ti.init(ti.metal)
    torch_device = torch.device("mps")

    substrate = Substrate(
        shape=shape,
        torch_dtype=torch.float32,
        torch_device=torch_device,
        channels={
            "bw": ti.f32,
        },
    )
    substrate.malloc()
    return substrate

def define_organism(substrate):
    sensors = ['bw']
    sensor_inds = substrate.windex[sensors]
    n_sensors = len(sensor_inds)
    return MinimalOrganism(n_sensors = n_sensors,
                            n_actuators = 1,
                            torch_device = substrate.torch_device)

def main():
    substrate = define_substrate(SHAPE)
    organism = define_organism(substrate)
    vis = MinimalVis(substrate, ["bw"])

    while vis.window.running:
        substrate.mem = organism.forward(substrate.mem)
        vis.update()
        if vis.perturbing_weights:
            organism.perturb_weights(vis.perturbation_strength)


if __name__ == "__main__":
    main()