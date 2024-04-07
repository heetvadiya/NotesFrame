// pages/[pdf].js

import { useRouter } from 'next/router';
import { useState, useEffect } from 'react';

const PDFPage = () => {
    const router = useRouter();
    const { pdf } = router.query;
    const [pdfData, setPdfData] = useState(null);

    //   useEffect(() => {
    //     const fetchPDFData = async () => {
    //       try {
    //         const res = await fetch(`/api/pdf/${pdf}`); // Assuming your API endpoint to fetch PDF data is /api/pdf/:pdfName
    //         const data = await res.blob();
    //         setPdfData(URL.createObjectURL(data));
    //       } catch (error) {
    //         console.error('Error fetching PDF data:', error);
    //       }
    //     };

    //     if (pdf) {
    //       fetchPDFData();
    //     }
    //   }, [pdf]);

    return (
        <div className='bg-gray-100 min-h-screen'>
            <div className="min-h-[80vh] bg-gray-100 flex justify-center items-center">
                <div className="bg-white rounded-lg shadow-lg overflow-hidden">
                    {!pdfData && (
                        <iframe
                            title="PDF Viewer"
                            src={pdfData}
                            width="800"
                            height="600"
                            frameBorder="0"
                            className="w-full h-full"
                        />
                    )}
                    {!pdfData && (
                        <div className="flex justify-center items-center py-10">
                            <p className="text-gray-600 text-lg">Loading PDF...</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default PDFPage;
