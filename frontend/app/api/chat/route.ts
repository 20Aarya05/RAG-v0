import { NextRequest, NextResponse } from 'next/server';
import Groq from 'groq-sdk';

const groq = new Groq({
  apiKey: process.env.GROQ_API_KEY,
});

export async function POST(request: NextRequest) {
  try {
    // Check if API key is available
    if (!process.env.GROQ_API_KEY) {
      console.error('GROQ_API_KEY is not set');
      return NextResponse.json(
        { error: 'API key not configured' },
        { status: 500 }
      );
    }

    const { message } = await request.json();

    if (!message) {
      return NextResponse.json(
        { error: 'Message is required' },
        { status: 400 }
      );
    }

    console.log('Sending message to Groq:', message);

    const chatCompletion = await groq.chat.completions.create({
      messages: [
        {
          role: 'system',
          content: 'You are a helpful AI assistant. Provide clear, concise, and helpful responses.',
        },
        {
          role: 'user',
          content: message,
        },
      ],
      model: 'llama-3.1-8b-instant',
      temperature: 0.7,
      max_tokens: 1024,
    });

    const responseMessage = chatCompletion.choices[0]?.message?.content || 'Sorry, I could not generate a response.';

    console.log('Received response from Groq:', responseMessage);

    return NextResponse.json({ message: responseMessage });
  } catch (error) {
    console.error('Groq API error:', error);
    
    // More detailed error logging
    if (error instanceof Error) {
      console.error('Error message:', error.message);
      console.error('Error stack:', error.stack);
    }
    
    return NextResponse.json(
      { error: 'Failed to process your request', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}