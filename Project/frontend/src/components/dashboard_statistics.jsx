import React from 'react';

/**
 * EmbeddedIframe Component
 * This component renders an iframe with the given properties.
 * @returns {JSX.Element} The iframe element to be rendered.
 */
const DashboardStatisticts = () => {
    return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
            <iframe 
                width="1000" 
                height="750" 
                src="https://lookerstudio.google.com/embed/reporting/13db439a-53fe-4d32-9333-596d152f76ec/page/s0L6D" 
                frameborder="0" 
                style={{ border: '0' }} 
                allowFullScreen 
                sandbox="allow-storage-access-by-user-activation allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox">
            </iframe>
        </div>
    );
}

export default DashboardStatisticts;
