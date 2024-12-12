import json

def compute_membership(x, points):
    for i in range(len(points) - 1):
        x0, mu0 = points[i]
        x1, mu1 = points[i + 1]
        if x0 <= x <= x1:
            return mu0 if mu0 == mu1 else mu0 + (mu1 - mu0) * (x - x0) / (x1 - x0)
    return 0

def map_temperature_to_regulator(temperature_mu_values, transition_mapping):
    regulator_mu_values = {}

    for temp_term, temp_mu in temperature_mu_values.items():
        reg_term = transition_mapping[temp_term]
        regulator_mu_values[reg_term] = max(regulator_mu_values.get(reg_term, 0), temp_mu)
    
    print(f"Projected fuzzy set for regulator positions: {regulator_mu_values}\n")
    return regulator_mu_values

def fuzzify(input_value, fuzzy_set):
    mu_values = {}

    for term, points in fuzzy_set.items():
        mu_values[term] = round(compute_membership(input_value, points), 2)

    print(f"Fuzzification result for temperature {input_value}: {mu_values}\n")
    return mu_values

def defuzzify_mean_max(regulator_mu_values, fuzzy_set):
    max_mu = max(regulator_mu_values.values())
    x_values = []

    for term, mu in regulator_mu_values.items():
        if mu == max_mu:
            points = fuzzy_set[term]
            for i in range(len(points) - 1):
                x0, mu0 = points[i]
                x1, mu1 = points[i + 1]
                
                if (mu0 <= max_mu <= mu1) or (mu1 <= max_mu <= mu0):
                    x_values.append(x0) if mu0 == mu1 else x_values.append(x0 + (x1 - x0) * (max_mu - mu0) / (mu1 - mu0))
                        
    return sum(x_values) / len(x_values) if x_values else 0

def main(temperatures_json: str, regulator_json: str, transition_json: str, temperature_input: float):
    temperatures_set = json.loads(temperatures_json)
    regulator_set = json.loads(regulator_json)
    transition_mapping = json.loads(transition_json)

    temperature_mu_values = fuzzify(temperature_input, temperatures_set)
    regulator_mu_values = map_temperature_to_regulator(temperature_mu_values, transition_mapping)

    mean_max = defuzzify_mean_max(regulator_mu_values, regulator_set)

    print(f"Defuzzified regulator position using mean-max method: {mean_max}\n")

temperatures = """{
    "холодно": [
        [0, 1],
        [16, 1],
        [20, 0],
        [50, 0]
    ],
    "комфортно": [
        [16, 0],
        [20, 1],
        [22, 1],
        [26, 0]
    ],
    "жарко": [
        [0, 0],
        [22, 0],
        [26, 1],
        [50, 1]
    ]
}"""

regulator = """{
    "слабо": [
        [0, 1],
        [6, 1],
        [10, 0],
        [20, 0]
    ],
    "умеренно": [
        [6, 0],
        [10, 1],
        [12, 1],
        [16, 0]
    ],
    "интенсивно": [
        [0, 0],
        [12, 0],
        [16, 1],
        [20, 1]
    ]
}"""

transition = """{
    "холодно": "интенсивно",
    "комфортно": "умеренно",
    "жарко": "слабо"
}"""

if __name__ == "__main__":
    main(temperatures, regulator, transition, 25)