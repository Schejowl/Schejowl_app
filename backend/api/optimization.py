import numpy as np
import gurobipy as gp
from gurobipy import GRB

class TimeSlotOptimizer:
    def __init__(self, preference_matrix):

        self.k = 1
        self.matrix = preference_matrix
        self._build_new_model()

    def _build_new_model(self):
        self.p = np.array(self.matrix)
        self.num_people, self.num_time_slots = self.p.shape
        self.coverage_weight = 1-1/self.num_people
        self.preference_weight = 1/self.num_people
        self.model = gp.Model("TimeSlotSelection")
        self.y = self.model.addVars(self.num_time_slots, vtype=GRB.BINARY, name="y")
        self._build_model()        

    def _build_model(self):
        objective = gp.LinExpr()

        for j in range(self.num_time_slots):
            num_attending = gp.LinExpr()
            preference_score = gp.LinExpr()

            for i in range(self.num_people):
                availability = self.p[i, j]
                if availability > 0:
                    num_attending += 1
                preference_score += availability

            total_score = self.coverage_weight * num_attending + self.preference_weight * preference_score
            objective += total_score * self.y[j]

        self.model.setObjective(objective, GRB.MAXIMIZE)

        # Allow only consecutive 'k' slots to be selected
        max_start = self.num_time_slots - self.k + 1
        self.s = self.model.addVars(max_start, vtype=GRB.BINARY, name="start")

        # Ensure exactly one starting position is chosen
        self.model.addConstr(gp.quicksum(self.s[i] for i in range(max_start)) == 1, name="ChooseStart")

        # Link y[j] to the selected consecutive block
        for j in range(self.num_time_slots):
            relevant_starts = []
            for start in range(max_start):
                if start <= j < start + self.k:
                    relevant_starts.append(self.s[start])
            if relevant_starts:
                self.model.addConstr(self.y[j] <= gp.quicksum(relevant_starts), name=f"Link_{j}")
            else:
                self.model.addConstr(self.y[j] == 0, name=f"ZeroOut_{j}")

    def split_matrix(self):

        splitted_matrix = []
        for row in self.matrix:
            splitted_row = []
            for element in row:
                splitted_row.append(element)
                splitted_row.append(element)
            splitted_matrix.append(splitted_row)
        self.k = self.k*2
        self.matrix = splitted_matrix
        self._build_new_model()
        

    def change_entry_matrix(self, row, slot, preference):
        self.matrix[row][slot] = preference
        self._build_new_model()


    def optimize(self):
        self.model.optimize()
        if self.model.status == GRB.OPTIMAL:
            return {
                "selected_slots": [j for j in range(self.num_time_slots) if self.y[j].x > 0.5],
                "total_score": self.model.objVal
            }   

        return {
            "error": "No optimal solution found."
        }

#Example 

preference_matrix = [
    [0.6, 0.2, 1, 0.6],
    [1, 1, 1, 0.2],
    [1, 1, 0.2, 1],
    [1, 1, 1, 1]]

optimizer = TimeSlotOptimizer(preference_matrix)
resul = optimizer.optimize()
optimizer.split_matrix()
result = optimizer.optimize()

    #print(resul["selected_slots"])
print(f"Selected index: {resul['selected_slots']}")
print(f"Optimal preference score: {resul['total_score']}")

if "error" in result:
    print(result["error"])

else:
    #print(f"Optimal time slot(s) index: {result['selected_slots']}")
    print(f"Selected index: {result['selected_slots']}")
    print(f"Optimal preference score: {result['total_score']}")

