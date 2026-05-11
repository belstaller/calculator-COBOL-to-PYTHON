import { NextRequest, NextResponse } from 'next/server';
import { calculationController } from '@/src/interfaces/http/controllers/calculation-controller';

export async function GET() {
  const calculations = await calculationController.list();
  return NextResponse.json({ data: calculations }, { status: 200 });
}

export async function POST(request: NextRequest) {
  try {
    const body = (await request.json()) as {
      leftOperand?: number;
      rightOperand?: number;
      operation?: 'add' | 'subtract' | 'multiply' | 'divide';
    };

    if (
      typeof body.leftOperand !== 'number' ||
      typeof body.rightOperand !== 'number' ||
      typeof body.operation !== 'string'
    ) {
      return NextResponse.json({ error: 'Invalid request payload.' }, { status: 400 });
    }

    const created = await calculationController.create({
      leftOperand: body.leftOperand,
      rightOperand: body.rightOperand,
      operation: body.operation,
    });

    return NextResponse.json({ data: created }, { status: 201 });
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Unexpected error.';
    return NextResponse.json({ error: message }, { status: 400 });
  }
}
