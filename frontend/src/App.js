import logo from './logo.svg';
import './App.css';
import React, { useState } from 'react';
import { Input } from './components/ui/input';
import { Button } from './components/ui/button';

const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];
const hours = Array.from({ length: 12 }, (_, i) => `${i + 8}:00`); // 8 AM to 7 PM

export default function Schejowl() {
  const [name, setName] = useState('');
  const [availability, setAvailability] = useState({});
  const [bestSlots, setBestSlots] = useState([]);

  const toggleSlot = (day, hour) => {
    const key = `${day}-${hour}`;
    setAvailability((prev) => {
      const current = prev[key] || 0;
      const next = current >= 1 ? 0 : parseFloat((current + 0.2).toFixed(1));
      return {
        ...prev,
        [key]: next,
      };
    });
  };

  const getColor = (value) => {
    if (value === 0) return 'bg-white';
    if (value <= 0.2) return 'bg-green-100';
    if (value <= 0.4) return 'bg-green-200';
    if (value <= 0.6) return 'bg-green-300';
    if (value <= 0.8) return 'bg-green-400';
    return 'bg-green-500';
  };

  const handleSubmit = async () => {
    await fetch('http://127.0.0.1:8000/api/availability/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, availability }),
    });
  };

  const fetchOptimalSlot = async () => {
    const res = await fetch('http://127.0.0.1:8000/api/optimize/');
    const data = await res.json();
    if (data.selected_slots) {
      setBestSlots(data.selected_slots);
    } else {
      alert(data.error);
    }
  };

  return (
    <div className="max-w-5xl mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Schejowl</h1>

      <div className="mb-4 flex items-center gap-2">
        <Input
          placeholder="Your name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <Button onClick={handleSubmit}>Submit Availability</Button>
        <Button onClick={fetchOptimalSlot}>Find Best Time</Button>
      </div>

      <div className="grid grid-cols-[80px_repeat(5,1fr)] gap-px bg-gray-300">
        <div className="bg-white"></div>
        {days.map((day) => (
          <div key={day} className="bg-white text-center font-semibold">
            {day}
          </div>
        ))}

        {hours.map((hour, hourIdx) => (
          <React.Fragment key={hour}>
            <div className="bg-white text-sm flex items-center justify-center">
              {hour}
            </div>
            {days.map((day, dayIdx) => {
              const key = `${day}-${hour}`;
              const index = hourIdx * days.length + dayIdx;
              const value = availability[key] || 0;
              const isOptimized = bestSlots.includes(index);

              return (
                <div
                  key={key}
                  onClick={() => toggleSlot(day, hour)}
                  className={`h-10 cursor-pointer border ${getColor(value)}
                    ${isOptimized ? 'border-4 border-blue-500' : ''}`}
                ></div>
              );
            })}
          </React.Fragment>
        ))}
      </div>

      {/* Optional: Legend */}
      <div className="mt-4 text-sm text-gray-600">
        <p>Click slots to set preference (0 → 0.2 → 0.4 → 0.6 → 0.8 → 1 → 0)</p>
        <div className="flex gap-2 mt-2">
          <div className="w-8 h-4 bg-white border"></div> 0
          <div className="w-8 h-4 bg-green-100 border"></div> 0.2
          <div className="w-8 h-4 bg-green-200 border"></div> 0.4
          <div className="w-8 h-4 bg-green-300 border"></div> 0.6
          <div className="w-8 h-4 bg-green-400 border"></div> 0.8
          <div className="w-8 h-4 bg-green-500 border"></div> 1
        </div>
      </div>
    </div>
  );
}