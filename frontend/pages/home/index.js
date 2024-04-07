"use client";

import { Button } from "@/components/ui/button";
import { Loader2 } from "lucide-react";
import Head from "next/head";
import { useState } from "react";
import { FileUploader } from "react-drag-drop-files";

const fileTypes = ["JPG", "PNG", "GIF"];

export default function Page() {
    const [file, setFile] = useState();
    const [loading, setLoading] = useState(false);

    const handleFileChange = (file) => {
        setFile(file);
    }

    const handleUpload = async () => {
        setLoading(true);
        console.log("hello");
        //api
        setTimeout(() => {
            setLoading(false);
        }, 1000);
    }

    return (
        <div>
            <Head>
                <title>ML Video to PDF</title>
                <meta name="description" content="Convert your video to PDF notes with machine learning." />
                <link rel="icon" href="/favicon.ico" />
            </Head>

            <main className="bg-gray-100 min-h-screen flex flex-col justify-center items-center">
                <h1 className="text-4xl font-bold text-center mb-4">Convert Video to PDF Notes</h1>
                <p className="text-lg text-gray-700 text-center mb-8">Upload your video and get important notes extracted into a PDF.</p>
                <FileUploader handleChange={handleFileChange} name="file" types={fileTypes} />
                {
                    (loading) ? <div className="flex justify-center mt-7">
                        <Button disabled>
                            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                            Uploading...
                        </Button>
                    </div> : <div className="flex justify-center mt-7">
                        <Button className="w-full h-11 text-lg" onClick={handleUpload}>Upload Video</Button>
                    </div>
                }
            </main >

            <footer className="bg-gray-200 text-center py-4 mt-8">
                <p className="text-gray-600">© 2024 ML Video to PDF</p>
            </footer>
        </div >
    );
}
