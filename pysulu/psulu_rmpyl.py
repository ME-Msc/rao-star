"""Straight-line pSulu replacement for running the bundled examples."""
import math

import numpy as np

from rmpyl.episodes import Episode
from rmpyl.rmpyl import RMPyL


class PySuluRMPyL(object):
    def __init__(self, *args, **kwargs):
        self.last_input = {}

    def simple_stochastic_model(self, parameters, init_pos_var, process_pos_var, dim=2):
        return {
            "parameters": dict(parameters),
            "init_pos_var": init_pos_var,
            "process_pos_var": process_pos_var,
            "dim": dim,
        }

    def write_model_file(self, stoch_model):
        self.last_model = stoch_model

    def plan(self, start_state, goal_state, parameters, parse_output=True):
        start = np.array(start_state[:2], dtype=float)
        goal = np.array(goal_state[:2], dtype=float)
        dist = float(np.linalg.norm(goal - start))
        horizon = float(parameters.get("time_horizon", max(dist, 1.0)))
        waypoints = [
            tuple((start + (goal - start) * alpha).tolist()) + (0.0, 0.0)
            for alpha in np.linspace(0.0, 1.0, int(parameters.get("waypoints", 10)))
        ]
        sol_properties = {
            "distance": dist,
            "duration": horizon,
            "risk": parameters.get("chance_constraint", 0.0),
        }
        self.last_input = {
            "start_state": start_state,
            "goal_state": goal_state,
            "parameters": dict(parameters),
        }
        return sol_properties, waypoints

    def as_rmpyl(self, sol_properties, waypoints, duration_type="uniform",
                 psulu_input=None, agent="robot", **kwargs):
        start = np.array(waypoints[0][:2], dtype=float)
        goal = np.array(waypoints[-1][:2], dtype=float)
        dist = float(sol_properties.get("distance", np.linalg.norm(goal - start)))
        max_velocity = float((psulu_input or {}).get("parameters", {}).get("max_velocity", 1.0))
        avg_velocity = max(max_velocity * 0.5, 1e-6)
        lb_duration = dist / max(max_velocity, 1e-6)
        ub_duration = dist / avg_velocity

        if duration_type in ["uniform", "uncontrollable_probabilistic"]:
            duration = {
                "ctype": "uncontrollable_probabilistic",
                "distribution": {"type": "uniform", "lb": lb_duration, "ub": ub_duration},
            }
        elif duration_type == "gaussian":
            duration = {
                "ctype": "uncontrollable_probabilistic",
                "distribution": {
                    "type": "gaussian",
                    "mean": (lb_duration + ub_duration) / 2.0,
                    "variance": math.pow(max(ub_duration - lb_duration, 0.0), 2) / 36.0,
                },
            }
        elif duration_type == "uncontrollable_bounded":
            duration = {"ctype": "uncontrollable_bounded", "lb": lb_duration, "ub": ub_duration}
        else:
            duration = {"ctype": "controllable", "lb": 0.0, "ub": float("inf")}

        ep = Episode(
            duration=duration,
            action="(go-from-to %s %s %s)" % (agent, tuple(start), tuple(goal)),
            distance=dist,
            start_coords=start,
            goal_coords=goal,
            **kwargs
        )
        ep.properties["distance"] = dist
        ep.properties["start_coords"] = start
        ep.properties["goal_coords"] = goal
        prog = RMPyL()
        prog.plan = ep
        return prog

    def plan_episode(self, start_state, goal_state, parameters, stoch_model=None,
                     duration_type="uniform", agent="robot", **kwargs):
        sol_properties, waypoints = self.plan(start_state, goal_state, parameters)
        return self.as_rmpyl(
            sol_properties,
            waypoints,
            duration_type=duration_type,
            psulu_input=self.last_input,
            agent=agent,
            **kwargs
        ).plan
