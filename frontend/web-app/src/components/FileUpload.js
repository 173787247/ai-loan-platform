import React, { useState, useRef } from 'react';
import './FileUpload.css';

const FileUpload = ({ onFileUpload, onClose, isVisible }) => {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const supportedTypes = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'image/jpeg',
    'image/png',
    'image/jpg',
    'image/bmp',
    'image/tiff'
  ];

  const supportedExtensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.jpg', '.jpeg', '.png', '.bmp', '.tiff'];

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files);
    }
  };

  const handleFileInput = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFiles(e.target.files);
    }
  };

  const handleFiles = (files) => {
    const newFiles = Array.from(files).filter(file => {
      const isValidType = supportedTypes.includes(file.type) || 
                         supportedExtensions.some(ext => file.name.toLowerCase().endsWith(ext));
      if (!isValidType) {
        alert(`不支持的文件格式: ${file.name}\n支持的格式: PDF, Word, Excel, 图片`);
      }
      return isValidType;
    });

    setSelectedFiles(prev => [...prev, ...newFiles]);
  };

  const removeFile = (index) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const handleUpload = async () => {
    if (selectedFiles.length === 0) return;

    setUploading(true);
    try {
      for (const file of selectedFiles) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('category', 'loan_application');
        formData.append('metadata', JSON.stringify({
          uploadTime: new Date().toISOString(),
          fileType: file.type,
          fileSize: file.size
        }));

        const response = await fetch(`${process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'}/api/v1/rag/process-document`, {
          method: 'POST',
          body: formData
        });

        if (!response.ok) {
          throw new Error(`上传失败: ${response.statusText}`);
        }

        const result = await response.json();
        console.log('文件上传成功:', result);
      }

      // 通知父组件上传完成
      onFileUpload(selectedFiles);
      setSelectedFiles([]);
      onClose();
    } catch (error) {
      console.error('文件上传失败:', error);
      alert(`上传失败: ${error.message}`);
    } finally {
      setUploading(false);
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getFileIcon = (fileType) => {
    if (fileType.includes('pdf')) return '📄';
    if (fileType.includes('word') || fileType.includes('document')) return '📝';
    if (fileType.includes('excel') || fileType.includes('sheet')) return '📊';
    if (fileType.includes('image')) return '🖼️';
    return '📎';
  };

  if (!isVisible) return null;

  return (
    <div className="file-upload-overlay">
      <div className="file-upload-modal">
        <div className="file-upload-header">
          <h3>📎 上传贷款申请材料</h3>
          <button className="close-btn" onClick={onClose}>✖️</button>
        </div>

        <div className="file-upload-content">
          <div className="upload-instructions">
            <p>请上传您的贷款申请相关材料：</p>
            <ul>
              <li>📄 身份证、营业执照等证件（PDF/图片）</li>
              <li>📊 财务报表、银行流水（Excel/PDF）</li>
              <li>📝 贷款申请书、合同等（Word/PDF）</li>
              <li>🖼️ 其他相关材料（支持拍照OCR识别）</li>
            </ul>
          </div>

          <div 
            className={`upload-area ${dragActive ? 'drag-active' : ''}`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              ref={fileInputRef}
              type="file"
              multiple
              accept=".pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png,.bmp,.tiff"
              onChange={handleFileInput}
              style={{ display: 'none' }}
            />
            
            <div className="upload-icon">📁</div>
            <p>点击选择文件或拖拽文件到此处</p>
            <p className="upload-hint">支持 PDF, Word, Excel, 图片格式</p>
          </div>

          {selectedFiles.length > 0 && (
            <div className="selected-files">
              <h4>已选择的文件：</h4>
              {selectedFiles.map((file, index) => (
                <div key={index} className="file-item">
                  <span className="file-icon">{getFileIcon(file.type)}</span>
                  <div className="file-info">
                    <span className="file-name">{file.name}</span>
                    <span className="file-size">{formatFileSize(file.size)}</span>
                  </div>
                  <button 
                    className="remove-file-btn"
                    onClick={() => removeFile(index)}
                  >
                    ✖️
                  </button>
                </div>
              ))}
            </div>
          )}

          <div className="upload-actions">
            <button 
              className="upload-btn"
              onClick={handleUpload}
              disabled={selectedFiles.length === 0 || uploading}
            >
              {uploading ? '⏳ 上传中...' : `📤 上传 ${selectedFiles.length} 个文件`}
            </button>
            <button className="cancel-btn" onClick={onClose}>
              取消
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FileUpload;
