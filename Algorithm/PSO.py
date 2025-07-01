import numpy as np

class SensorPlacementPSO:
    def __init__(self, map_2d, coverage, iterations):
        self.map_2d = np.array(map_2d)
        self.coverage = coverage
        self.iterations = iterations
        self.rows, self.cols = self.map_2d.shape
        self.valid_positions = [(i, j) for i in range(self.rows) for j in range(self.cols) if self.map_2d[i][j] == 1]

    def fitness(self, positions):
        """Calculate fitness based on coverage and minimizing overlaps."""
        covered = set()
        for x, y in positions:
            for dx in range(-self.coverage, self.coverage + 1):
                for dy in range(-self.coverage, self.coverage + 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.rows and 0 <= ny < self.cols and self.map_2d[nx][ny] == 1:
                        covered.add((nx, ny))
        return len(covered)

    def optimize(self, num_particles=30):
        """Run the PSO optimization process."""
        particles = [np.random.choice(len(self.valid_positions), size=len(self.valid_positions) // 2, replace=False) for _ in range(num_particles)]
        velocities = [np.zeros_like(particle, dtype=float) for particle in particles]  # 수정: float 타입으로 초기화

        personal_best = particles[:]
        personal_best_scores = [self.fitness([self.valid_positions[i] for i in particle]) for particle in particles]

        global_best = personal_best[np.argmax(personal_best_scores)]
        global_best_score = max(personal_best_scores)

        for iteration in range(self.iterations):
            for i, particle in enumerate(particles):
                velocities[i] += np.random.uniform(0, 1) * (personal_best[i] - particle)
                velocities[i] += np.random.uniform(0, 1) * (global_best - particle)
                particles[i] = np.clip(particle + velocities[i].astype(int), 0, len(self.valid_positions) - 1)  # 수정: int로 변환

                unique_positions = set(particles[i])
                positions = [self.valid_positions[idx] for idx in unique_positions]
                score = self.fitness(positions)

                if score > personal_best_scores[i]:
                    personal_best[i] = particles[i]
                    personal_best_scores[i] = score

                if score > global_best_score:
                    global_best = particles[i]
                    global_best_score = score

            print(f"Iteration {iteration + 1}/{self.iterations}, Best Score: {global_best_score}")

        best_positions = [self.valid_positions[idx] for idx in global_best]
        return best_positions
