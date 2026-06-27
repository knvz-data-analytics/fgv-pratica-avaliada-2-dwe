using Microsoft.AspNetCore.Mvc;
using ApiProdutos.Models;
using System.Collections.Generic;
using System.Linq;

namespace ApiProdutos.Controllers
{
    // [ApiController] ativa comportamentos especificos
    // como validação automática das DataAnnotations (400 Bad Request se falhar).
    [Route("api/[controller]")]
    [ApiController]
    public class ProdutosController : ControllerBase
    {
        // Simulando um banco de dados na memória para o funcionamento dos endpoints
        private static readonly List<Produto> _produtos = new List<Produto>();
        private static int _nextId = 1;

        // 1. Endpoint: GET: Retornando a lista completa de Produtos
        [HttpGet]
        public ActionResult<IEnumerable<Produto>> Get()
        {
            return Ok(_produtos); // Retorna HTTP 200 OK
        }

        // 2. Endpoint: GET/{id}: Retorna um Produto pelo ID especifico
        [HttpGet("{id}")]
        public ActionResult<Produto> GetById(int id)
        {
            var produto = _produtos.FirstOrDefault(p => p.Id == id);

            if (produto == null)
            {
                return NotFound(new {mensagem = "Produto não encontrado."}); // Retorna HTTP 404
            }

            return Ok(produto); // Retorna HTTP 200 OK

        }

        // 3. Endpoint: POST: Cria um novo Produto
        [HttpPost]
        public ActionResult<Produto> Post([FromBody] Produto produto)
        {
            // Atribui um ID ao novo produto e adiciona a lista
            produto.Id = _nextId++;
            _produtos.Add(produto);

            return CreatedAtAction(nameof(GetById), new
            {
                id = produto.Id
            }, produto);
        }
    }
}