using System;
using GeneticSharp.Domain;
using GeneticSharp.Domain.Crossovers;
using GeneticSharp.Domain.Fitnesses;
using GeneticSharp.Domain.Mutations;
using GeneticSharp.Domain.Selections;
using GeneticSharp.Infrastructure.Framework.Threading;
using MySql.Data.MySqlClient;

namespace Integradora2
{
    class Program
    {
        static void Main(string[] args)
        {
            ConnectDb();

            /*
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
            */
        }

        static void ConnectDb()
        {
            var user = Environment.GetEnvironmentVariable("integradora_user", EnvironmentVariableTarget.User);
            var password = Environment.GetEnvironmentVariable("integradora_password", EnvironmentVariableTarget.User);
            var connectionStr = $"Server=localhost;Uid={user};Pwd={password};Database=tpch;";
            using var connection = new MySqlConnection(connectionStr);
            connection.Open();
            var query = "SELECT C_MKTSEGMENT FROM tpch.customer where C_CUSTKEY=10;";
            var queryCmd = new MySqlCommand(query, connection);

            var result = queryCmd.ExecuteScalar().ToString();
            Console.WriteLine(result);
        }
    }
}
