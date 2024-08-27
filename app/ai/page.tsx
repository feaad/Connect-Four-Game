import Banner from '@/components/Banner';
import Form from '@/components/Form';
import Link from 'next/link';
import React from 'react'
import Button from '@/components/Button';
import Modal from './components/Modal';
import axios from "axios";

import { Algorithm } from '@/types/types';

import { env } from '@/lib/env';

async function Algorithms() {
  let algorithms: Algorithm[] = [];
  try {
    const response = await axios.get(
      `${env.API_URL}/algorithm`,
    );
    if (response.data.length > 0) {
      algorithms = response.data;
    }
  } catch (error) {
    console.error(error);
  }

  return (
    <>
      {algorithms.map((algorithm) => (
        <Modal algorithm={algorithm.code_name} key={algorithm.algorithm_id} />
      ))}
    </>
  )

}

const AIPage = () => {

  return (
    <div className="grid h-screen grid-cols-2 gap-16">
      <Banner />
      <div>
        
        {/* <Form title="Play with AI" description="First pick a nickname" /> */}

        <div className="pt-20">
          <h1 className="font sans pb-2 font-medium">
            Which Game Master do you want to play against?
          </h1>
          <Algorithms />
        </div>
      </div>
    </div>
  );
}

export default AIPage