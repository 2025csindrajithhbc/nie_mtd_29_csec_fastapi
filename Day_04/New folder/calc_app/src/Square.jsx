
import { useState } from "react"

export default function Squre() {
    const [num, setNum] = useState(0);
    const [sqr, setSqr] = useState(0);
    return (
        <>
            <p>
                Number: <input
                    type="number"
                    value={num}
                    onChange={(e) => {setNum(parseInt(e.target.value)); }}
                /> </p>
            <p><button onClick={() => { setSqr(Number(num) * Number(num)); }}>Calculate</button></p>
            <p>Square of {num} is {sqr}</p>
        </>
    )
}

