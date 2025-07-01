# STEAM

## _Project Information_
- Performed by DXLAB at Gyeongsang National University
- Supported by National Research Foundation
- Duration: 2023.04.01. - 2027.12.31.

## _Contributors_
- Seonghyeon Moon(Project Director)
- <strong>Yutak Seo</strong>
- Haejun Seong
- Seokhye Lee
- Seungwon Shin

## _Collaboration_
- Seoul National University
- SmartInside AI
- Glotechsoft
- POSCO E&C

## _Genetic Algorithm for Sensor Deployment Optimization_
**Genetic Algorithms** (GA) are based on an **evolutionary approach** to AI, in which methods of the evolution of a population is used to obtain an optimal solution for a given problem. They were proposed in 1975 by [John Henry Holland](https://wikipedia.org/wiki/John_Henry_Holland).

Genetic Algorithms are based on the following ideas:

* Valid solutions to the problem can be represented as **genes**
* **Crossover** allows us to combine two solutions together to obtain a new valid solution
* **Selection** is used to select more optimal solutions using some **fitness function**
* **Mutations** are introduced to destabilize optimization and get us out of the local minimum

If you want to implement a Genetic Algorithm, you need the following:

 * To find a method of coding our problem solutions using **genes** g&in;&Gamma;
 * On the set of genes &Gamma; we need to define **fitness function** fit: &Gamma;&rightarrow;**R**. Smaller function values correspond to better solutions.
 * To define **crossover** mechanism to combine two genes together to get a new valid solution crossover: &Gamma;<sup>2</sub>&rightarrow;&Gamma;.
 * To define **mutation** mechanism mutate: &Gamma;&rightarrow;&Gamma;.

In many cases, crossover and mutation are quite simple algorithms to manipulate genes as numeric sequences or bit vectors.

The specific implementation of a genetic algorithm can vary from case to case, but the overall structure is the following:

1. Select an initial population G&subset;&Gamma;
2. Randomly select one of the operations that will be performed at this step: crossover or mutation
3. **Crossover**:
  * Randomly select two genes g<sub>1</sub>, g<sub>2</sub> &in; G
  * Compute crossover g=crossover(g<sub>1</sub>,g<sub>2</sub>)
  * If fit(g)<fit(g<sub>1</sub>) or fit(g)<fit(g<sub>2</sub>) - replace corresponding gene in the population by g.
4. **Mutation** - select random gene g&in;G and replace it by mutate(g)
5. Repeat from step 2, until we get a sufficiently small value of fit, or until the limit on the number of steps is reached.

## _Typical Tasks_

Tasks typically solved by Genetic Algorithms include:

1. Schedule optimization
2. Optimal packing
3. Optimal cutting
4. Speeding up exhaustive search


source: [Dmitry Soshnikov, PhD](https://soshnikov.com/) (2024) "Genetic Algorithm", _AI For Beginners_, https://github.com/microsoft/AI-For-Beginners

## _Research Framework_
![Research Framework](__framework_img.png)

## <strong>Usage</strong>
### 1. _Map_

### 2. _HarrisCorner_

### 3. _GeneticAlgorithm_

### 4. _SensorModule_

### 5. _PlotTools_
