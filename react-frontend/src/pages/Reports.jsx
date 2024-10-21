import React from 'react';
import { BsFillArchiveFill, BsFillGrid3X3GapFill, BsPeopleFill, BsFillBellFill } from 'react-icons/bs';
import { GiGiftOfKnowledge } from "react-icons/gi";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@material-ui/core';

function Reports() {

    const interviewReport = [
        {
          id: 1,
          interviewer: 'John Doe',
          candidate: 'Jane Smith',
          position: 'Software Engineer',
          date: '2022-01-01',
          rating: 4.5,
          feedback: 'Great candidate, very knowledgeable about the field.',
        },
        {
          id: 2,
          interviewer: 'Jane Smith',
          candidate: 'Bob Johnson',
          position: 'Product Manager',
          date: '2022-01-05',
          rating: 4.2,
          feedback: 'Good candidate, but lacked experience in the field.',
        },
        {
          id: 3,
          interviewer: 'Bob Johnson',
          candidate: 'Alice Brown',
          position: 'UX Designer',
          date: '2022-01-10',
          rating: 4.8,
          feedback: 'Excellent candidate, very creative and talented.',
        },
        {
          id: 4,
          interviewer: 'Alice Brown',
          candidate: 'Mike Davis',
          position: 'DevOps Engineer',
          date: '2022-01-15',
          rating: 4.6,
          feedback: 'Good candidate, but needed more experience with cloud computing.',
        },
    ];

  return (
    <main className='main-container'>
        <div className='main-title'>
            <h3 className='alpha'>INTERVIEW REPORT</h3>
        </div>

        <div className='main-cards'>
            <div className='card'>
                <div className='card-inner'>
                    <h3>Total Interviews</h3>
                    <BsPeopleFill />
                </div>
                <h1>10</h1>
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
                    <h3>Most Recent Interview</h3>
                    <BsFillGrid3X3GapFill />
                </div>
                <h1>2022-01-15</h1>
            </div>
            <div className='card'>
                <div className='card-inner'>
                    <h3>Oldest Interview</h3>
                    <BsFillArchiveFill />
                </div>
                <h1>2022-01-01</h1>
            </div>
        </div>

        <div className='table-container'>
            <TableContainer>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Interviewer</TableCell>
                            <TableCell>Candidate</TableCell>
                            <TableCell>Position</TableCell>
                            <TableCell>Date</TableCell>
                            <TableCell>Rating</TableCell>
                            <TableCell>Feedback</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {interviewReport.map((report) => (
                            <TableRow key={report.id}>
                                <TableCell>{report.interviewer}</TableCell>
                                <TableCell>{report.candidate}</TableCell>
                                <TableCell>{report.position}</TableCell>
                                <TableCell>{report.date}</TableCell>
                                <TableCell>{report.rating}</TableCell>
                                <TableCell>{report.feedback}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </div>
    </main>
  )
}

export default Reports;