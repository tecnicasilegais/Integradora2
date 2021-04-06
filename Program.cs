using System;
using GeneticSharp.Domain;
using GeneticSharp.Domain.Crossovers;
using GeneticSharp.Domain.Fitnesses;
using GeneticSharp.Domain.Mutations;
using GeneticSharp.Domain.Selections;
using GeneticSharp.Infrastructure.Framework.Threading;

namespace Integradora2
{
    class Program
    {
        static void Main(string[] args)
        {
            var taskExecutor = new ParallelTaskExecutor();
            taskExecutor.MinThreads = 4;
            taskExecutor.MaxThreads = 11;


            var crossover = new TwoPointCrossover();
            var selection = new TournamentSelection(5);
            var mutation = new FlipBitMutation();
            var ga = new GeneticAlgorithm();

            ga.MutationProbability = 0.2f;
            ga.CrossoverProbability = 0.65f;


            ga.TaskExecutor = taskExecutor;
        }
    }
}
