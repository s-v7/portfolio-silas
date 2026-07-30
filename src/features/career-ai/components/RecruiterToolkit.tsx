import { QRCodeCanvas } from "qrcode.react";

const CV_URL = "https://s-v7.github.io/portfolio-silas/curriculo.pdf";

export function RecruiterToolkit() {
  return (
    <section className="recruiter-toolkit">
      <div className="toolkit-mini">
        <a className="toolkit-mini__qr" href={CV_URL} target="_blank" rel="noreferrer">
          <QRCodeCanvas value={CV_URL} size={72} />
        </a>

        <div>
          <strong>CV PDF</strong>
          <small>Scan ou download</small>
        </div>
      </div>
    </section>
  );
}
