import React from 'react';
import { BsFillArchiveFill, BsFillGrid3X3GapFill, BsPeopleFill, BsFillBellFill } from 'react-icons/bs';
import { GiGiftOfKnowledge } from "react-icons/gi";
import { BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';

function Home() {

    const data = [
        {
          name: 'Mock Interview 1',
          uv: 4000,
          pv: 2400,
          amt: 2400,
        },
        {
          name: 'Mock Interview 2',
          uv: 3000,
          pv: 1398,
          amt: 2210,
        },
        {
          name: 'Mock Interview 3',
          uv: 2000,
          pv: 9800,
          amt: 2290,
        },
        {
          name: 'Mock Interview 4',
          uv: 2780,
          pv: 3908,
          amt: 2000,
        },
        {
          name: 'Mock Interview 5',
          uv: 1890,
          pv: 4800,
          amt: 2181,
        },
        {
          name: 'Mock Interview 6',
          uv: 2390,
          pv: 3800,
          amt: 2500,
        },
        {
          name: 'Mock Interview 7',
          uv: 3490,
          pv: 4300,
          amt: 2100,
        },
      ];

  return (
    <main className='main-container'>
        <div className='main-title'>
            <h3 className='alpha'>MOCKMATE DASHBOARD</h3>
        </div>

        <div className='main-cards'>
            <div className='card'>
                <div className='card-inner'>
                    <h3>Total Interviews</h3>
                    <BsPeopleFill />
                </div>
                <h1>300</h1>
            </div>
            <div className='card'>
                <div className='card-inner'>
                    <h3>Average Rating</h3>
                    <GiGiftOfKnowledge />
                </div>
                <h1>4.5/5</h1>
            </div>
            <div className='card'>
                <div className='card-inner'>
                    <h3>Completed Interviews</h3>
                    <BsFillArchiveFill />
                </div>
                <h1>250</h1>
            </div>
            <div className='card'>
                <div className='card-inner'>
                    <h3>Upcoming Interviews</h3>
                    <BsFillBellFill />
                </div>
                <h1>50</h1>
            </div>
        </div>

        <div className='charts'>
            <ResponsiveContainer width="100%" height="100%">
            <BarChart
            width={500}
            height={300}
            data={data}
            margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 5,
            }}
            >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="pv" fill="#8884d8" />
                <Bar dataKey="uv" fill="#82ca9d" />
                </BarChart>
            </ResponsiveContainer>

            <ResponsiveContainer width="100%" height="100%">
                <LineChart
                width={500}
                height={300}
                data={data}
                margin={{
                    top: 5,
                    right: 30,
                    left: 20,
                    bottom: 5,
                }}
                >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="pv" stroke="#8884d8" activeDot={{ r: 8 }} />
                <Line type="monotone" dataKey="uv" stroke="#82ca9d" />
                </LineChart>
            </ResponsiveContainer>

        </div>
    </main>
  )
}

export default Home