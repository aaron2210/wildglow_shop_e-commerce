export const Ofrecemos = () => {
    return (
        <>
            <div className="container-fluid bg-light-pink py-5">
                <div className="row mb-4">
                    <div className="col-12 text-center">
                        <h5 className="fw-bold">Ofrecemos</h5>
                        <p>
                            Productos hechos con dedicación, aromas que inspiran y un servicio
                            <br/>pensado para hacerte sentir especial en cada detalle.
                        </p>
                    </div>
                </div>
                <div className="row justify-content-center text-center g-4">
                    
                    <div className="col-12 col-md-6 col-lg-4">
                        <div className="service-card p-4 rounded-4 h-100">
                            <div className="icon-circle mb-3">
                                <i className="fa-solid fa-hanukiah fa-2x"></i>
                            </div>
                            <h6>Amplia variedad de productos</h6>
                            <p>Tenemos algo especial para <br />cada rincón de tu hogar.</p>
                        </div>
                    </div>

                    
                    <div className="col-12 col-md-6 col-lg-4">
                        <div className="service-card p-4 rounded-4 h-100">
                            <div className="icon-circle mb-3">
                                <i className="fa-solid fa-truck-fast fa-2x"></i>
                            </div>
                            <h6>Envío gratuito y rápido</h6>
                            <p>Empacamos con cuidado y enviamos <br />con cariño, directo a tu puerta.</p>
                        </div>
                    </div>

                    
                    <div className="col-12 col-md-6 col-lg-4">
                        <div className="service-card p-4 rounded-4 h-100">
                            <div className="icon-circle mb-3">
                                <i className="fa-solid fa-phone fa-2x"></i>
                            </div>
                            <h6>Atención personalizada</h6>
                            <p>Te acompañamos antes, durante <br />y después de tu compra.</p>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}