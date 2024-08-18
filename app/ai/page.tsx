import Banner from '@/components/Banner';
import Form from '@/components/Form';
import Link from 'next/link';
import React from 'react'
import Button from '@/components/Button';

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
          <Button label="Mystic" link="" />
          <Button label="Sphinx" link="" />
        </div>
      </div>
    </div>
  );
}

export default AIPage