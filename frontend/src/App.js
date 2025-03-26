import React, { useState, useEffect } from "react";
import axios from "axios";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

const App = () => {
  const [data, setData] = useState([]);
  const [moeda, setMoeda] = useState("BRL");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/api/cotacoes/buscar/`, 
          {
            params: {
              moeda: moeda,
              dias: 5
            },
            headers: {
              'Accept': 'application/json',
            }
          }
        );
        
        // Formata os dados para o grafico
        const formattedData = response.data.map(item => ({
          ...item,
          data: new Date(item.data).toLocaleDateString('pt-BR'),
          valor: parseFloat(item.valor)
        })).reverse(); // Inverte para mostrar do mais antigo para o mais recente
        
        setData(formattedData);
      } catch (err) {
        console.error("Erro na requisiçao:", err);
        setError("Erro ao carregar dados. Tente novamente.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [moeda]);

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1 style={{ textAlign: 'center' }}>Cotações do {moeda}</h1>
      
      <div style={{ margin: '20px 0', textAlign: 'center' }}>
        <select 
          onChange={(e) => setMoeda(e.target.value)}
          style={{ padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
        >
          <option value="BRL">Real (BRL)</option>
          <option value="EUR">Euro (EUR)</option>
          <option value="JPY">Iene Japonês (JPY)</option>
        </select>
      </div>

      {loading && <p style={{ textAlign: 'center' }}>Carregando...</p>}
      {error && <p style={{ textAlign: 'center', color: 'red' }}>{error}</p>}
      
      {data.length > 0 && (
        <div style={{ height: '400px' }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={data}
              margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="data" />
              <YAxis domain={['auto', 'auto']} />
              <Tooltip 
                formatter={(value) => [value.toFixed(4), 'Valor']}
                labelFormatter={(label) => `Data: ${label}`}
              />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="valor" 
                stroke="#8884d8" 
                activeDot={{ r: 8 }}
                name={`USD para ${moeda}`}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
};

export default App;