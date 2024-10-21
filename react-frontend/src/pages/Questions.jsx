import React from 'react';
import { BsFillArchiveFill, BsFillGrid3X3GapFill, BsPeopleFill, BsFillBellFill } from 'react-icons/bs';
import { GiGiftOfKnowledge } from "react-icons/gi";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@material-ui/core';

function Questions() {

    const questions = [
        {
          id: 1,
          question: 'What is your greatest strength?',
          category: 'Behavioral',
          difficulty: 'Easy',
          frequency: 80,
        },
        {
          id: 2,
          question: 'How do you handle stress?',
          category: 'Behavioral',
          difficulty: 'Medium',
          frequency: 60,
        },
        {
          id: 3,
          question: 'What is the difference between monolithic architecture and microservices architecture?',
          category: 'Technical',
          difficulty: 'Hard',
          frequency: 40,
        },
        {
          id: 4,
          question: 'Can you explain the concept of Big O notation?',
          category: 'Technical',
          difficulty: 'Hard',
          frequency: 30,
        },
        {
          id: 5,
          question: 'Why do you want to work for our company?',
          category: 'Behavioral',
          difficulty: 'Easy',
          frequency: 90,
        },
        {
          id: 6,
          question: 'How do you prioritize tasks?',
          category: 'Behavioral',
          difficulty: 'Medium',
          frequency: 70,
        },
        {
          id: 7,
          question: 'What is your experience with Agile development?',
          category: 'Technical',
          difficulty: 'Medium',
          frequency: 50,
        },
        {
          id: 8,
          question: 'Can you describe a time when you had to troubleshoot a difficult technical issue?',
          category: 'Behavioral',
          difficulty: 'Hard',
          frequency: 20,
        },
    ];

  return (
    <main className='main-container'>
        <div className='main-title'>
            <h3 className='alpha'>INTERVIEW QUESTIONS</h3>
        </div>

        <div className='main-cards'>
            <div className='card'>
                <div className='card-inner'>
                    <h3>Total Questions</h3>
                    <BsPeopleFill />
                </div>
                <h1>100</h1>
            </div>
            <div className='card'>
                <div className='card-inner'>
                    <h3>Most Frequently Asked</h3>
                    <GiGiftOfKnowledge />
                </div>
                <h1>What is your greatest strength?</h1>
            </div>
            <div className='card'>
                <div className='card-inner'>
                    <h3>Most Difficult</h3>
                    <BsFillGrid3X3GapFill />
                </div>
                <h1>Can you explain the concept of Big O notation?</h1>
            </div>
            <div className='card'>
                <div className='card-inner'>
                    <h3>Least Frequently Asked</h3>
                    <BsFillArchiveFill />
                </div>
                <h1>Can you describe a time when you had to troubleshoot a difficult technical issue?</h1>
            </div>
        </div>

        <div className='table-container'>
            <TableContainer>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Question</TableCell>
                            <TableCell>Category</TableCell>
                            <TableCell>Difficulty</TableCell>
                            <TableCell>Frequency</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {questions.map((question) => (
                            <TableRow key={question.id}>
                                <TableCell>{question.question}</TableCell>
                                <TableCell>{question.category}</TableCell>
                                <TableCell>{question.difficulty}</TableCell>
                                <TableCell>{question.frequency}%</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </div>
    </main>
  )
}

export default Questions;