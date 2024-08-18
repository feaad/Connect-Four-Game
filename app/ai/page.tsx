import Banner from '@/components/Banner';
import Form from '@/components/Form';
import Link from 'next/link';
import React from 'react'
import Button from '@/components/Button';
import Modal from '@/components/GenericModal';

const AIPage = () => {
  return (
    <div className="grid h-screen grid-cols-2 gap-16">
      <Banner />
      <div>
        <Form title="Play with AI" description="First pick a nickname" />

        <div className="pt-20">
          <h1 className="font sans pb-2 font-medium">
            Which Game Master do you want to play against?
          </h1>
          <Modal title="Mystic" />
          <Modal title="Sphinx" />
          
        </div>
      </div>
    </div>
  );
}

export default AIPage