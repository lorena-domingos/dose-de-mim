import React, { useState, useEffect } from "react";
import DatePicker from "react-datepicker";
import {registerLocale} from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import ptBR from "date-fns/locale/pt-BR";
import { format, parseISO } from 'date-fns';

registerLocale('pt-BR', ptBR)

function App() {
  const [entries, setEntries] = useState([]);
  const [selectedDate, setSelectedDate] = useState(null);

  useEffect(() => {
    fetch('http://localhost:5000/api/diarios')
      .then(res => res.json())
      .then(data => setEntries(data))
      .catch(err => console.error('Erro ao carregar entradas:', err));
  }, []);

  const highlightDates = entries.map(e => {
    const [year, month, day] = e.date.split('-');
    return new Date(year, month - 1, day, 12);
  });

  const filteredEntries = selectedDate
    ? entries.filter(e => e.date === selectedDate.toISOString().split("T")[0])
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

      <ul>
        {filteredEntries.map((e, i) => {
          const dataFormatada = e.date ? format(parseISO(e.date), 'dd/MM/yyyy') : 'Data inválida';
          return <li key={i}>{dataFormatada}: {e.texto}</li>;
        })}
      </ul>
    </div>
  );
}

export default App;
