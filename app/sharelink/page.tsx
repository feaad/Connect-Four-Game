import Banner from '@/components/Banner'
import Form from '@/components/Form';
import Link from 'next/link';
import React from 'react'

const ShareLink = () => {
  return (
    <div className="grid h-screen grid-cols-2 gap-16">
      <Banner />
      <div>
        <Form title="Play with a friend" description="First pick a nickname" />

        <div className="pt-20">
          <h1 className="font sans font-medium pb-2">
            Share this link with your friend
          </h1>
          <Link href="/share-link" className='font-sans font-normal text-slate-400 text-2xl bg-slate-100 '>
            https://playwithfriend/connectfour/Kitara
          </Link>
        </div>
      </div>
    </div>
  );
}

export default ShareLink