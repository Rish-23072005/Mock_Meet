import React from 'react';
import { BsFillArchiveFill, BsFillGrid3X3GapFill, BsPeopleFill, BsFillBellFill } from 'react-icons/bs';
import { GiGiftOfKnowledge } from "react-icons/gi";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@material-ui/core';

function Interviewers() {

    const interviewers = [
        {
          id: 1,
          name: 'John Doe',
          role: 'Software Engineer',
          rating: 4.5,
          interviews: 10,
        },
        {
          id: 2,
          name: 'Jane Smith',
          role: 'Product Manager',
          rating: 4.8,
          interviews: 8,
        },
        {
          id: 3,
          name: 'Bob Johnson',
          role: 'Data Scientist',
          rating: 4.2,
          interviews: 12,
        },
        {
          id: 4,
          name: 'Alice Brown',
          role: 'UX Designer',
          rating: 4.9,
          interviews: 9,
        },
        {
          id: 5,
          name: 'Mike Davis',
          role: 'DevOps Engineer',
          rating: 4.6,
          interviews: 11,
        },
    ];

  return (
    <main className='main-container'>
        <div className='main-title'>
            <h3 className='alpha'>INTERVIEWERS</h3>
        </div>

        <div className='main-cards'>
            <div className='card'>
                <div className='card-inner'>
                    <h3>Total Interviewers</h3>
                    <BsPeopleFill />
                </div>
                <h1>50</h1>
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
                    <h3>Most Experienced</h3>
                    <BsFillGrid3X3GapFill />
                </div>
                <h1>Bob Johnson</h1>
            </div>
            <div className='card'>
                <div className='card-inner'>
                    <h3>Least Experienced</h3>
                    <BsFillArchiveFill />
                </div>
                <h1>Alice Brown</h1>
            </div>
        </div>

        <div className='table-container'>
            <TableContainer>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Name</TableCell>
                            <TableCell>Role</TableCell>
                            <TableCell>Rating</TableCell>
                            <TableCell>Interviews</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {interviewers.map((interviewer) => (
                            <TableRow key={interviewer.id}>
                                <TableCell>{interviewer.name}</TableCell>
                                <TableCell>{interviewer.role}</TableCell>
                                <TableCell>{interviewer.rating}</TableCell>
                                <TableCell>{interviewer.interviews}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </div>
    </main>
  )
}

export default Interviewers;