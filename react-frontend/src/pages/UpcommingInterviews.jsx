import React from 'react';
import { BsFillArchiveFill, BsFillGrid3X3GapFill, BsPeopleFill, BsFillBellFill } from 'react-icons/bs';
import { GiGiftOfKnowledge } from "react-icons/gi";
import { BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';

function UpcomingInterview() {

    const data = [
        {
          name: 'Week 1',
          upcoming: 5,
          rating: 4.2,
        },
        {
          name: 'Week 2',
          upcoming: 7,
          rating: 4.5,
        },
        {
          name: 'Week 3',
          upcoming: 3,
          rating: 4.0,
        },
        {
          name: 'Week 4',
          upcoming: 9,
          rating: 4.8,
        },
        {
          name: 'Week 5',
          upcoming: 6,
          rating: 4.3,
        },
        {
          name: 'Week 6',
          upcoming: 4,
          rating: 4.1,
        },
        {
          name: 'Week 7',
          upcoming: 8,
          rating: 4.6,
        },
      ];

  return (
    <main className='main-container'>
        <div className='main-title'>
            <h3 className='alpha'>UPCOMING INTERVIEWS</h3>
        </div>

        <div className='main-cards'>
            <div className='card'>
                <div className='card-inner'>
                    <h3>Total Upcoming Interviews</h3>
                    <BsPeopleFill />
                </div>
                <h1>40</h1>
            </div>
            <div className='card'>
                <div className='card-inner'>
                    <h3>Average Rating</h3>
                    <GiGiftOfKnowledge />
                </div>
                <h1>4.4/5</h1>
            </div>
            <div className='card'>
                <div className='card-inner'>
                    <h3>Most Popular Week</h3>
                    <BsFillGrid3X3GapFill />
                </div>
                <h1>Week 4</h1>
            </div>
            <div className='card'>
                <div className='card-inner'>
                    <h3>Least Popular Week</h3>
                    <BsFillArchiveFill />
                </div>
                <h1>Week 3</h1>
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
                <Bar dataKey="upcoming" fill="#8884d8" />
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
                <Line type="monotone" dataKey="rating" stroke="#82ca9d" activeDot={{ r: 8 }} />
                </LineChart>
            </ResponsiveContainer>

        </div>
    </main>
  )
}

export default UpcomingInterview;