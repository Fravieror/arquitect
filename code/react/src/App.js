import React from 'react';

function App(){
  var oldStyleVar = "I'm using var";

  let name = "John";
  let age = 30;
  let salary = 75000.50;
  let isEmployed = true;

  const PI = 3.14159;
  const COMPANY = "TechCorp";

  const person = {firstName: "Jane", lastName: "Doe"};
  const numbers = [1,2,3,4,5];

  const greeting = `Hello, ${name}! you are ${age} years old.`;

  let nullValue = null;
  let undefinedValue;

  const {firstName, lastName} = person;
  const [first, second, ...rest] = numbers;

  // short circuit evaluation
  const shortcircuit = {
    andShort: false && 'never reached', // false
    orShort: 'value' || 'default', // 'value'
    orDefault: '' || 'default',
    nullishCoalescing: null ?? 'default',
    nullishZero: 0 ?? 'default',
  }

  //ternary operators
  ternaryResult = 10>1 ? 'x': 'y';


  return (
    <div style={{padding: '20px', fontFamily: 'monospace'}}>
      <h1>Javascript variables demo</h1>
      <h2>basic variables</h2>
      <p>name: {name}</p>
      <p>age: {age}</p>
      <p>salary: ${salary.toFixed(2)}</p>
      <p>employed: {isEmployed.toString()}</p>

      <h2>Constants</h2>
      <p>PI: {PI}</p>
      <p>Company: {COMPANY}</p>

      <h2>Template Literal</h2>
      <p>{greeting}</p>

      <h2>Object & array</h2>
      <p>person: {firstName} {lastName}</p>
      <p>numbers: {numbers.join(', ')}</p>
      
      <h2>Destructuring</h2>
      <p>First: {first}, second: {second}</p>
      <p>rest: {rest.join(', ')}</p>

      <h2>type checking</h2>
      <p>typeof name: {typeof name}</p>
      <p>typeof age: {typeof age}</p>
      <p>typeof isEmployed: {typeof isEmployed}</p>
      <p>typeof person: {typeof person}</p>
      <p>typeof numbers: {typeof numbers} (Array.isArray: {Array.isArray(numbers).toString()})</p>
    </div>
  );
}

export default App;
