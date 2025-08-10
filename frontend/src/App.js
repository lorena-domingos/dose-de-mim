import React, { useState, useEffect } from "react";
import DatePicker from "react-datepicker";
import {registerLocale} from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import ptBR from "date-fns/locale/pt-BR";
import { format, parseISO } from 'date-fns';

registerLocale('pt-BR', ptBR)

function App() {
  const [dados, setDados] = useState({ remedios: [], diarios: [] });
  const [selectedDate, setSelectedDate] = useState(null);

  useEffect(() => {
    fetch('http://localhost:5000/api/dados')
      .then(res => res.json())
      .then(data => setDados(data))
      .catch(err => console.error('Erro ao carregar entradas:', err));
  }, []);

  const highlightDates = [
    ...dados.diarios,
    ...dados.remedios
  ]

  .filter(e => e.date || e.data)
    .map(e => {
      const dataStr = e.date || e.data;
      const [year, month, day] = dataStr.split('-');
      return new Date(year, month - 1, day, 12);
    });

    const filteredDiarios = selectedDate
    ? dados.diarios.filter(d => d.date === selectedDate.toISOString().split("T")[0])
    : [];

  const filteredRemedios = selectedDate
    ? dados.remedios.filter(r => r.data === selectedDate.toISOString().split("T")[0])
    : [];

  return (
    <div class="calendario" style={{ padding: "20px" }}>
      <h2>Calendário</h2>

      <DatePicker
        selected={selectedDate}
        onChange={(date) => setSelectedDate(date)}
        highlightDates={highlightDates}
        locale="pt-BR"
        dateFormat="dd-MM-yyyy"
        placeholderText="Escolha uma data"
      />

      {selectedDate && (
        <>
          <h3>Entradas de Diário</h3>
          {filteredDiarios.length > 0 ? (
            <ul>
              {filteredDiarios.map((e, i) => {
                const dataFormatada = e.date ? format(parseISO(e.date), 'dd/MM/yyyy') : 'Data inválida';
                return <li key={i}>{dataFormatada}: {e.texto}</li>;
              })}
            </ul>
          ) : (
            <p>Nenhuma entrada de diário para essa data.</p>
          )}

          <h3>Registros de Remédio</h3>
          {filteredRemedios.length > 0 ? (
            <ul>
              {filteredRemedios.map((e, i) => {
                const dataFormatada = e.data ? format(parseISO(e.data), 'dd/MM/yyyy') : 'Data inválida';
                return <li key={i}>{dataFormatada}: {e.tomou ? 'Tomou' : 'Não tomou'}</li>;
              })}
            </ul>
          ) : (
            <p>Nenhum registro de remédio para essa data.</p>
          )}
        </>
      )}
    </div>
  );
}

export default App;
